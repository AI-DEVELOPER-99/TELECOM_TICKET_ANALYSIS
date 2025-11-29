import json
from typing import List, Dict
from config import Config
from vector_store import VectorStoreManager

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class TicketAnalysisAgent:
    """AI agent for analyzing tickets and suggesting solutions"""
    
    def __init__(self, vector_store: VectorStoreManager):
        """
        Initialize the ticket analysis agent
        
        Args:
            vector_store: Initialized VectorStoreManager instance
        """
        self.config = Config()
        self.vector_store = vector_store
        self.use_openai = self.config.LLM_MODE == 'openai'
        
        if self.use_openai:
            if OpenAI is None:
                raise ImportError("OpenAI not installed. Run: pip install openai")
            if not self.config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in .env file")
            self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
            print("Using OpenAI for solution generation")
        else:
            print("Using local rule-based solution generation")
    
    def analyze_ticket(self, ticket_description: str) -> Dict:
        """
        Analyze a ticket and suggest top 3 solutions with suitability percentages
        
        Args:
            ticket_description: The new ticket description
            
        Returns:
            Dictionary containing suggested solutions with rankings
        """
        # Step 1: Find similar resolved tickets
        print("Searching for similar tickets...")
        similar_tickets = self.vector_store.search_similar_tickets(
            ticket_description, 
            top_k=self.config.TOP_K_RESULTS
        )
        
        # Step 2: Prepare context for LLM
        context = self._prepare_context(similar_tickets)
        
        # Step 3: Generate solutions using LLM
        print("Generating solutions...")
        if self.use_openai:
            solutions = self._generate_solutions_openai(ticket_description, context, similar_tickets)
        else:
            solutions = self._generate_solutions_local(ticket_description, similar_tickets)
        
        return {
            'query': ticket_description,
            'solutions': solutions,
            'similar_tickets_count': len(similar_tickets)
        }
    
    def _prepare_context(self, similar_tickets: List[Dict]) -> str:
        """
        Prepare context string from similar tickets for LLM
        
        Args:
            similar_tickets: List of similar tickets with metadata
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, ticket in enumerate(similar_tickets, 1):
            context_part = f"""
--- Similar Ticket {i} (Similarity: {ticket['similarity_score']:.2%}) ---
Subject: {ticket['subject']}
Description: {ticket['body'][:500]}...
Type: {ticket['type']}
Priority: {ticket['priority']}
Resolution: {ticket['answer']}
"""
            context_parts.append(context_part)
        
        return "\n".join(context_parts)
    
    def _generate_solutions_local(self, query: str, similar_tickets: List[Dict]) -> List[Dict]:
        """
        Generate solutions using local rule-based approach (no API needed)
        
        Args:
            query: The new ticket description
            similar_tickets: List of similar tickets
            
        Returns:
            List of 3 solutions with suitability percentages
        """
        solutions = []
        
        # Take top 3 most similar tickets and use their solutions
        for i, ticket in enumerate(similar_tickets[:3], 1):
            similarity_score = ticket['similarity_score']
            suitability = int(similarity_score * 100)
            
            # Extract the solution from the answer field
            answer = ticket['answer']
            
            # Create reasoning based on similarity and ticket attributes
            reasoning = f"This solution is based on a {ticket['type']} ticket with {similarity_score:.1%} similarity. "
            reasoning += f"The original issue had {ticket['priority']} priority "
            reasoning += f"and was resolved through the {ticket['queue']} queue. "
            reasoning += f"The matching ticket dealt with a similar problem in the same category."
            
            solutions.append({
                'rank': i,
                'solution': answer,
                'suitability_percentage': suitability,
                'reasoning': reasoning,
                'reference_tickets': [i]
            })
        
        return solutions
    
    def _generate_solutions_openai(self, query: str, context: str, similar_tickets: List[Dict]) -> List[Dict]:
        """
        Use OpenAI LLM to generate and rank top 3 solutions
        
        Args:
            query: The new ticket description
            context: Context from similar tickets
            similar_tickets: List of similar tickets
            
        Returns:
            List of 3 solutions with suitability percentages
        """
        system_prompt = """You are an expert technical support AI assistant for a telecom service provider.
Your task is to analyze a new support ticket and suggest the top 3 most suitable solutions based on similar resolved tickets.

For each solution:
1. Provide a clear, actionable solution description
2. Assign a suitability percentage (0-100%) indicating how well this solution addresses the issue
3. Explain the reasoning behind the suggestion
4. Reference which similar ticket(s) informed this solution

Requirements:
- The three suitability percentages should be in descending order
- Solutions should be distinct and not redundant
- Be specific and actionable
- Consider the ticket type, priority, and technical context

Return your response as a JSON array with exactly 3 solutions, each containing:
- "solution": string (the solution description)
- "suitability_percentage": number (0-100)
- "reasoning": string (why this solution is suitable)
- "reference_tickets": array of numbers (indices of similar tickets used, 1-based)
"""

        user_prompt = f"""New Support Ticket:
{query}

Similar Resolved Tickets for Context:
{context}

Based on these similar resolved tickets, suggest the top 3 solutions for the new ticket. 
Return ONLY a valid JSON array with exactly 3 solution objects, no additional text."""

        try:
            response = self.client.chat.completions.create(
                model=self.config.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            
            response_text = response.choices[0].message.content
            
            # Parse JSON response
            try:
                # Try to parse as direct array
                solutions = json.loads(response_text)
                
                # If it's wrapped in an object, extract the array
                if isinstance(solutions, dict):
                    # Look for common keys that might contain the array
                    for key in ['solutions', 'results', 'recommendations', 'suggestions']:
                        if key in solutions and isinstance(solutions[key], list):
                            solutions = solutions[key]
                            break
                
                # Validate we have exactly 3 solutions
                if not isinstance(solutions, list) or len(solutions) < 3:
                    raise ValueError("Invalid response format")
                
                # Take only top 3
                solutions = solutions[:3]
                
                # Ensure all required fields are present and normalize
                normalized_solutions = []
                for i, sol in enumerate(solutions, 1):
                    normalized_solutions.append({
                        'rank': i,
                        'solution': sol.get('solution', 'Solution not provided'),
                        'suitability_percentage': min(100, max(0, sol.get('suitability_percentage', 0))),
                        'reasoning': sol.get('reasoning', 'Reasoning not provided'),
                        'reference_tickets': sol.get('reference_tickets', [])
                    })
                
                return normalized_solutions
                
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"Error parsing LLM response: {e}")
                print(f"Response text: {response_text}")
                return self._generate_fallback_solutions(similar_tickets)
        
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return self._generate_fallback_solutions(similar_tickets)
    
    def _generate_fallback_solutions(self, similar_tickets: List[Dict]) -> List[Dict]:
        """
        Generate fallback solutions if LLM fails
        
        Args:
            similar_tickets: List of similar tickets
            
        Returns:
            List of 3 fallback solutions
        """
        solutions = []
        
        for i, ticket in enumerate(similar_tickets[:3], 1):
            similarity_score = ticket['similarity_score']
            suitability = int(similarity_score * 100)
            
            solutions.append({
                'rank': i,
                'solution': ticket['answer'][:500] + '...' if len(ticket['answer']) > 500 else ticket['answer'],
                'suitability_percentage': suitability,
                'reasoning': f"Based on a similar {ticket['type']} ticket with {similarity_score:.1%} similarity",
                'reference_tickets': [i]
            })
        
        return solutions

def format_analysis_result(result: Dict) -> str:
    """
    Format the analysis result for display
    
    Args:
        result: Analysis result dictionary
        
    Returns:
        Formatted string
    """
    output = []
    output.append("=" * 80)
    output.append("TICKET ANALYSIS RESULTS")
    output.append("=" * 80)
    output.append(f"\nQuery: {result['query'][:200]}...")
    output.append(f"\nAnalyzed based on {result['similar_tickets_count']} similar resolved tickets\n")
    output.append("\n" + "=" * 80)
    output.append("TOP 3 RECOMMENDED SOLUTIONS")
    output.append("=" * 80)
    
    for solution in result['solutions']:
        output.append(f"\n{solution['rank']}. SOLUTION (Suitability: {solution['suitability_percentage']}%)")
        output.append("-" * 80)
        output.append(f"\n{solution['solution']}\n")
        output.append(f"REASONING: {solution['reasoning']}")
        if solution['reference_tickets']:
            output.append(f"REFERENCES: Similar tickets #{', #'.join(map(str, solution['reference_tickets']))}")
        output.append("")
    
    output.append("=" * 80)
    
    return "\n".join(output)

if __name__ == "__main__":
    # Test the analysis agent
    print("Initializing system...")
    vector_store = VectorStoreManager(use_openai=True)
    vector_store.build_vector_store()
    
    agent = TicketAnalysisAgent(vector_store)
    
    # Test query
    test_ticket = """
    Subject: Cannot access company VPN from home
    
    Description: I'm trying to connect to the company VPN from my home network but keep getting 
    connection timeout errors. I've tried restarting my router and computer, but the issue persists.
    The VPN client shows "connecting" for about 30 seconds then fails with error code 800.
    This is urgent as I need to access internal systems for work.
    """
    
    print("\n\nAnalyzing ticket...\n")
    result = agent.analyze_ticket(test_ticket)
    
    print(format_analysis_result(result))

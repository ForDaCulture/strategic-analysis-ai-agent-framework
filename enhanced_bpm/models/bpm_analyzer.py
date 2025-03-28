"""
BPM Analyzer - Core analysis engine for Business Process Management insights.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class BPMAnalyzer:
    """
    Business Process Management Analyzer that provides detailed insights
    based on industry data and BPM principles.
    """
    
    def __init__(self, data_dir: str = "../data"):
        """
        Initialize the BPM Analyzer with data from the specified directory.
        
        Args:
            data_dir: Path to the directory containing BPM and industry data files
        """
        self.data_dir = data_dir
        self.bpm_principles = self._load_json("bpm_principles.json")
        self.industry_data = {}
        self.load_available_industries()
        self.current_industry = None
        
    def load_available_industries(self) -> List[str]:
        """
        Load all available industry data files.
        
        Returns:
            List of available industry names
        """
        industry_files = [f for f in os.listdir(self.data_dir) 
                         if f.endswith("_industry.json")]
        
        available_industries = []
        for file in industry_files:
            industry_name = file.replace("_industry.json", "").replace("_", " ")
            self.industry_data[industry_name] = None  # Lazy loading
            available_industries.append(industry_name)
            
        return available_industries
    
    def set_current_industry(self, industry_name: str) -> bool:
        """
        Set the current industry for analysis.
        
        Args:
            industry_name: Name of the industry to analyze
            
        Returns:
            True if industry was successfully set, False otherwise
        """
        normalized_name = industry_name.lower().replace(" ", "_")
        file_path = f"{normalized_name}_industry.json"
        
        if normalized_name in [k.lower().replace(" ", "_") for k in self.industry_data.keys()]:
            # Load the industry data if not already loaded
            if self.industry_data[industry_name] is None:
                self.industry_data[industry_name] = self._load_json(file_path)
            
            self.current_industry = industry_name
            return True
        
        return False
    
    def get_industry_overview(self) -> Dict[str, Any]:
        """
        Get a comprehensive overview of the current industry.
        
        Returns:
            Dictionary containing industry overview information
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return {"error": "No industry selected or data not available"}
        
        industry_data = self.industry_data[self.current_industry]
        
        return {
            "name": industry_data["industry_name"],
            "description": industry_data["industry_overview"]["description"],
            "market_size": industry_data["industry_overview"]["market_size"],
            "key_segments": industry_data["industry_overview"]["key_segments"],
            "drivers": industry_data["industry_overview"]["industry_drivers"],
            "challenges": industry_data["industry_overview"]["challenges"]
        }
    
    def analyze_porter_five_forces(self) -> Dict[str, Any]:
        """
        Analyze the industry using Porter's Five Forces framework.
        
        Returns:
            Dictionary containing Porter's Five Forces analysis
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return {"error": "No industry selected or data not available"}
        
        industry_data = self.industry_data[self.current_industry]
        
        # Get the Porter's Five Forces analysis from the industry data
        five_forces = industry_data["porter_five_forces_analysis"]
        
        # Get the BPM framework information for Porter's Five Forces
        bpm_framework = next((f for f in self.bpm_principles["frameworks"] 
                             if f["name"] == "Porter's Five Forces"), None)
        
        # Combine the industry-specific analysis with the general framework
        result = {
            "framework_description": bpm_framework["description"] if bpm_framework else "",
            "forces": {}
        }
        
        for force in five_forces:
            result["forces"][force] = {
                "level": five_forces[force]["level"],
                "factors": five_forces[force]["factors"],
                "process_implications": five_forces[force]["process_implications"]
            }
            
        return result
    
    def analyze_balanced_scorecard(self) -> Dict[str, Any]:
        """
        Analyze the industry using the Balanced Scorecard framework.
        
        Returns:
            Dictionary containing Balanced Scorecard analysis
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return {"error": "No industry selected or data not available"}
        
        industry_data = self.industry_data[self.current_industry]
        
        # Get the Balanced Scorecard analysis from the industry data
        bsc = industry_data["balanced_scorecard_analysis"]
        
        # Get the BPM framework information for Balanced Scorecard
        bpm_framework = next((f for f in self.bpm_principles["frameworks"] 
                             if f["name"] == "Balanced Scorecard"), None)
        
        # Combine the industry-specific analysis with the general framework
        result = {
            "framework_description": bpm_framework["description"] if bpm_framework else "",
            "perspectives": {}
        }
        
        for perspective in bsc:
            result["perspectives"][perspective] = {
                "objectives": bsc[perspective]["key_objectives"],
                "metrics": bsc[perspective]["key_metrics"],
                "maturity_assessment": bsc[perspective]["process_maturity_assessment"]
            }
            
        return result
    
    def get_process_optimization_recommendations(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get process optimization recommendations for the current industry.
        
        Returns:
            Dictionary containing short, medium, and long-term recommendations
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return {"error": "No industry selected or data not available"}
        
        industry_data = self.industry_data[self.current_industry]
        
        # Get the process optimization recommendations from the industry data
        recommendations = industry_data["process_optimization_recommendations"]
        
        return {
            "short_term": recommendations["short_term_improvements"],
            "medium_term": recommendations["medium_term_transformations"],
            "long_term": recommendations["long_term_strategic_innovations"]
        }
    
    def analyze_value_chain(self) -> Dict[str, Any]:
        """
        Analyze the industry value chain.
        
        Returns:
            Dictionary containing value chain analysis
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return {"error": "No industry selected or data not available"}
        
        industry_data = self.industry_data[self.current_industry]
        
        # Get the value chain analysis from the industry data
        value_chain = industry_data["value_chain_analysis"]
        
        # Get the BPM framework information for Value Chain Analysis
        bpm_framework = next((f for f in self.bpm_principles["frameworks"] 
                             if f["name"] == "Value Chain Analysis"), None)
        
        # Combine the industry-specific analysis with the general framework
        result = {
            "framework_description": bpm_framework["description"] if bpm_framework else "",
            "activities": value_chain
        }
            
        return result
    
    def get_competitive_landscape(self) -> Dict[str, Any]:
        """
        Get the competitive landscape of the current industry.
        
        Returns:
            Dictionary containing competitive landscape information
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return {"error": "No industry selected or data not available"}
        
        industry_data = self.industry_data[self.current_industry]
        
        return industry_data["competitive_landscape"]
    
    def get_business_process_analysis(self) -> Dict[str, Any]:
        """
        Get the business process analysis for the current industry.
        
        Returns:
            Dictionary containing business process analysis
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return {"error": "No industry selected or data not available"}
        
        industry_data = self.industry_data[self.current_industry]
        
        return industry_data["business_process_analysis"]
    
    def get_bpm_principles(self) -> Dict[str, Any]:
        """
        Get the core BPM principles.
        
        Returns:
            Dictionary containing BPM principles
        """
        return {
            "core_principles": self.bpm_principles["core_principles"],
            "methodologies": self.bpm_principles["methodologies"],
            "maturity_models": self.bpm_principles["maturity_models"]
        }
    
    def get_bpm_performance_metrics(self) -> Dict[str, Any]:
        """
        Get BPM performance metrics by category.
        
        Returns:
            Dictionary containing BPM performance metrics
        """
        return {
            "metrics_by_category": self.bpm_principles["performance_metrics"]
        }
    
    def get_bpm_implementation_practices(self) -> Dict[str, Any]:
        """
        Get BPM implementation best practices.
        
        Returns:
            Dictionary containing BPM implementation best practices
        """
        return {
            "best_practices": self.bpm_principles["implementation_best_practices"],
            "common_challenges": self.bpm_principles["common_challenges"]
        }
    
    def get_technology_enablers(self) -> Dict[str, Any]:
        """
        Get BPM technology enablers.
        
        Returns:
            Dictionary containing BPM technology enablers
        """
        return {
            "enablers": self.bpm_principles["technology_enablers"]
        }
    
    def search_across_data(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search across all data for the given query.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary containing search results by category
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return {"error": "No industry selected or data not available"}
        
        query = query.lower()
        results = {
            "industry_overview": [],
            "competitive_landscape": [],
            "value_chain": [],
            "business_processes": [],
            "porter_five_forces": [],
            "balanced_scorecard": [],
            "recommendations": []
        }
        
        # Helper function to search in nested dictionaries
        def search_dict(d, path="", results_list=None):
            if results_list is None:
                results_list = []
                
            if isinstance(d, dict):
                for k, v in d.items():
                    new_path = f"{path}.{k}" if path else k
                    if isinstance(v, (dict, list)):
                        search_dict(v, new_path, results_list)
                    elif isinstance(v, str) and query in v.lower():
                        results_list.append({
                            "path": new_path,
                            "content": v,
                            "context": k
                        })
            elif isinstance(d, list):
                for i, item in enumerate(d):
                    new_path = f"{path}[{i}]"
                    if isinstance(item, (dict, list)):
                        search_dict(item, new_path, results_list)
                    elif isinstance(item, str) and query in item.lower():
                        results_list.append({
                            "path": new_path,
                            "content": item,
                            "context": "List item"
                        })
            
            return results_list
        
        # Search in each section
        industry_data = self.industry_data[self.current_industry]
        
        results["industry_overview"] = search_dict(industry_data["industry_overview"])
        results["competitive_landscape"] = search_dict(industry_data["competitive_landscape"])
        results["value_chain"] = search_dict(industry_data["value_chain_analysis"])
        results["business_processes"] = search_dict(industry_data["business_process_analysis"])
        results["porter_five_forces"] = search_dict(industry_data["porter_five_forces_analysis"])
        results["balanced_scorecard"] = search_dict(industry_data["balanced_scorecard_analysis"])
        results["recommendations"] = search_dict(industry_data["process_optimization_recommendations"])
        
        # Filter out empty result categories
        return {k: v for k, v in results.items() if v}
    
    def answer_question(self, question: str) -> str:
        """
        Answer a specific question about the current industry using the available data.
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question based on available data
        """
        if not self.current_industry or not self.industry_data[self.current_industry]:
            return "No industry selected or data not available. Please select an industry first."
        
        # Convert question to lowercase for easier matching
        question_lower = question.lower()
        
        # Define patterns to match different types of questions
        patterns = [
            # Market size and growth
            (r"market size|how big|market value|industry size", self._answer_market_size),
            
            # Key players and competition
            (r"key players|competitors|leading companies|market leaders|who are the", self._answer_key_players),
            
            # Challenges and drivers
            (r"challenges|difficulties|problems|obstacles", self._answer_challenges),
            (r"drivers|growth factors|what drives|catalysts", self._answer_drivers),
            
            # Porter's Five Forces
            (r"porter|five forces|competitive forces|industry rivalry", self._answer_porter),
            (r"threat of new entrants|new entrants|barriers to entry", 
             lambda: self._answer_specific_force("threat_of_new_entrants")),
            (r"bargaining power of suppliers|supplier power|suppliers", 
             lambda: self._answer_specific_force("bargaining_power_of_suppliers")),
            (r"bargaining power of buyers|buyer power|customers", 
             lambda: self._answer_specific_force("bargaining_power_of_buyers")),
            (r"threat of substitutes|substitutes|alternative products", 
             lambda: self._answer_specific_force("threat_of_substitutes")),
            (r"industry rivalry|competition intensity|competitive landscape", 
             lambda: self._answer_specific_force("industry_rivalry")),
            
            # Balanced Scorecard
            (r"balanced scorecard|bsc|performance measurement", self._answer_balanced_scorecard),
            (r"financial perspective|financial metrics|financial performance", 
             lambda: self._answer_specific_perspective("financial_perspective")),
            (r"customer perspective|customer metrics|customer satisfaction", 
             lambda: self._answer_specific_perspective("customer_perspective")),
            (r"internal process|process perspective|internal business", 
             lambda: self._answer_specific_perspective("internal_process_perspective")),
            (r"learning and growth|innovation perspective|learning perspective", 
             lambda: self._answer_specific_perspective("learning_and_growth_perspective")),
            
            # Process optimization
            (r"process optimization|improve processes|process improvement|recommendations", 
             self._answer_process_recommendations),
            (r"short term|quick wins|immediate improvements", 
             lambda: self._answer_specific_recommendations("short_term")),
            (r"medium term|mid term|intermediate improvements", 
             lambda: self._answer_specific_recommendations("medium_term")),
            (r"long term|strategic improvements|future state", 
             lambda: self._answer_specific_recommendations("long_term")),
            
            # Value chain
            (r"value chain|primary activities|support activities", self._answer_value_chain),
            
            # BPM principles
            (r"bpm principles|core principles|process management principles", self._answer_bpm_principles),
            
            # BPM methodologies
            (r"methodologies|six sigma|lean|business process reengineering|bpr|tqm", 
             self._answer_bpm_methodologies),
            
            # Technology enablers
            (r"technology|software|tools|systems|enablers", self._answer_technology_enablers),
            
            # Performance metrics
            (r"metrics|kpis|performance indicators|measurements", self._answer_performance_metrics),
            
            # Implementation practices
            (r"implementation|best practices|how to implement|adoption", self._answer_implementation_practices),
            
            # Challenges in BPM
            (r"common challenges|difficulties in bpm|problems with bpm", self._answer_bpm_challenges)
        ]
        
        # Try to match the question to a pattern and get the answer
        for pattern, answer_func in patterns:
            if re.search(pattern, question_lower):
                return answer_func()
        
        # If no pattern matches, perform a general search
        search_results = self.search_across_data(question_lower)
        if search_results and not isinstance(search_results, dict) or not search_results.get("error"):
            # Compile relevant information from search results
            answer = f"Based on my analysis of the {self.current_industry} industry, here's what I found about '{question}':\n\n"
            
            for category, results in search_results.items():
                if results:
                    category_name = category.replace("_", " ").title()
                    answer += f"From {category_name}:\n"
                    for result in results[:3]:  # Limit to top 3 results per category
                        answer += f"- {result['content']}\n"
                    answer += "\n"
            
            return answer
        
        # If no information is found
        return (f"I don't have specific information to answer your question about '{question}' "
                f"for the {self.current_industry} industry. Please try asking in a different way or "
                f"ask about another aspect of the industry.")
    
    def _answer_market_size(self) -> str:
        """Answer questions about market size and growth."""
        industry_data = self.industry_data[self.current_industry]
        market_size = industry_data["industry_overview"]["market_size"]
        
        answer = f"# Market Size and Growth for the {self.current_industry.title()} Industry\n\n"
        answer += f"The global {self.current_industry} industry is valued at {market_size['global_value']} "
        answer += f"with a projected growth rate of {market_size['projected_growth']}.\n\n"
        
        answer += "## Key Markets\n"
        for market in market_size["key_markets"]:
            answer += f"- {market}\n"
        
        answer += "\n## Market Segments\n"
        for segment in industry_data["industry_overview"]["key_segments"]:
            answer += f"- {segment['name']}: {segment['description']}\n"
            answer += f"  - Market share: {segment['market_share']}\n"
            answer += f"  - Growth rate: {segment['growth_rate']}\n\n"
        
        return answer
    
    def _answer_key_players(self) -> str:
        """Answer questions about key players and competition."""
        industry_data = self.industry_data[self.current_industry]
        competitive_landscape = industry_data["competitive_landscape"]
        
        answer = f"# Competitive Landscape of the {self.current_industry.title()} Industry\n\n"
        answer += f"The {self.current_industry} industry has {competitive_landscape['market_concentration']} "
        answer += "market concentration.\n\n"
        
        answer += "## Key Players\n"
        for player in competitive_landscape["key_players"]:
            answer += f"### {player['name']} ({player['headquarters']})\n"
            answer += f"- Market share: {player['market_share']}\n"
            answer += "- Key strengths:\n"
            for strength in player["key_strengths"]:
                answer += f"  - {strength}\n"
            answer += "- Key weaknesses:\n"
            for weakness in player["key_weaknesses"]:
                answer += f"  - {weakness}\n\n"
        
        answer += "## New Entrants\n"
        for entrant in competitive_landscape["new_entrants"]:
            answer += f"### {entrant['name']}\n"
            answer += f"- Focus: {entrant['focus']}\n"
            answer += f"- Funding: {entrant['funding']}\n"
            answer += f"- Strengths: {entrant['strengths']}\n"
            answer += f"- Challenges: {entrant['challenges']}\n\n"
        
        answer += "## Strategic Partnerships\n"
        for partnership in competitive_landscape["strategic_partnerships"]:
            partners = ", ".join(partnership["partners"])
            answer += f"- {partners}: {partnership['focus']}\n"
        
        return answer
    
    def _answer_challenges(self) -> str:
        """Answer questions about industry challenges."""
        industry_data = self.industry_data[self.current_industry]
        challenges = industry_data["industry_overview"]["challenges"]
        
        answer = f"# Key Challenges in the {self.current_industry.title()} Industry\n\n"
        
        for challenge in challenges:
            answer += f"## {challenge['challenge']}\n"
            answer += f"{challenge['description']}\n"
            answer += f"Impact: {challenge['impact']}\n\n"
        
        # Add process-specific challenges
        answer += "# Process-Specific Challenges\n\n"
        
        business_processes = industry_data["business_process_analysis"]
        for process_area, details in business_processes.items():
            if "key_challenges" in details:
                answer += f"## {process_area.replace('_', ' ').title()}\n"
                for challenge in details["key_challenges"]:
                    answer += f"### {challenge['challenge']}\n"
                    answer += f"{challenge['description']}\n"
                    answer += "Process implications:\n"
                    for implication in challenge["process_implications"]:
                        answer += f"- {implication}\n"
                    answer += "\n"
        
        return answer
    
    def _answer_drivers(self) -> str:
        """Answer questions about industry drivers."""
        industry_data = self.industry_data[self.current_industry]
        drivers = industry_data["industry_overview"]["industry_drivers"]
        
        answer = f"# Key Drivers in the {self.current_industry.title()} Industry\n\n"
        
        for driver in drivers:
            answer += f"## {driver['factor']}\n"
            answer += f"{driver['description']}\n"
            answer += f"Impact: {driver['impact']}\n\n"
        
        return answer
    
    def _answer_porter(self) -> str:
        """Answer questions about Porter's Five Forces."""
        porter_analysis = self.analyze_porter_five_forces()
        
        answer = f"# Porter's Five Forces Analysis for the {self.current_industry.title()} Industry\n\n"
        answer += f"{porter_analysis['framework_description']}\n\n"
        
        for force, details in porter_analysis["forces"].items():
            force_name = force.replace("_", " ").title()
            answer += f"## {force_name}\n"
            answer += f"Level: {details['level']}\n\n"
            
            answer += "### Key Factors\n"
            for factor in details["factors"]:
                answer += f"- **{factor['factor']}**: {factor['description']}\n"
                answer += f"  - Impact: {factor['impact']}\n"
            
            answer += "\n### Process Implications\n"
            for implication in details["process_implications"]:
                answer += f"- {implication}\n"
            
            answer += "\n"
        
        return answer
    
    def _answer_specific_force(self, force: str) -> str:
        """Answer questions about a specific Porter's Five Force."""
        porter_analysis = self.analyze_porter_five_forces()
        
        if force not in porter_analysis["forces"]:
            return f"I don't have information about {force} for the {self.current_industry} industry."
        
        force_details = porter_analysis["forces"][force]
        force_name = force.replace("_", " ").title()
        
        answer = f"# {force_name} in the {self.current_industry.title()} Industry\n\n"
        answer += f"Level: {force_details['level']}\n\n"
        
        answer += "## Key Factors\n"
        for factor in force_details["factors"]:
            answer += f"### {factor['factor']}\n"
            answer += f"{factor['description']}\n"
            answer += f"Impact: {factor['impact']}\n\n"
        
        answer += "## Process Implications\n"
        for implication in force_details["process_implications"]:
            answer += f"- {implication}\n"
        
        return answer
    
    def _answer_balanced_scorecard(self) -> str:
        """Answer questions about Balanced Scorecard."""
        bsc_analysis = self.analyze_balanced_scorecard()
        
        answer = f"# Balanced Scorecard Analysis for the {self.current_industry.title()} Industry\n\n"
        answer += f"{bsc_analysis['framework_description']}\n\n"
        
        for perspective, details in bsc_analysis["perspectives"].items():
            perspective_name = perspective.replace("_", " ").title()
            answer += f"## {perspective_name}\n\n"
            
            answer += "### Key Objectives\n"
            for objective in details["objectives"]:
                answer += f"- {objective}\n"
            
            answer += "\n### Key Metrics\n"
            for metric in details["metrics"]:
                answer += f"#### {metric['metric']}\n"
                answer += f"{metric['description']}\n"
                answer += f"Industry benchmark: {metric['industry_benchmark']}\n"
                answer += "Process implications: " + metric['process_implications'] + "\n\n"
            
            answer += "### Process Maturity Assessment\n"
            maturity = details["maturity_assessment"]
            answer += f"Current state: {maturity['current_state']}\n\n"
            
            answer += "Challenges:\n"
            for challenge in maturity["challenges"]:
                answer += f"- {challenge}\n"
            
            answer += "\nImprovement opportunities:\n"
            for opportunity in maturity["improvement_opportunities"]:
                answer += f"- {opportunity}\n"
            
            answer += "\n"
        
        return answer
    
    def _answer_specific_perspective(self, perspective: str) -> str:
        """Answer questions about a specific Balanced Scorecard perspective."""
        bsc_analysis = self.analyze_balanced_scorecard()
        
        if perspective not in bsc_analysis["perspectives"]:
            return f"I don't have information about {perspective} for the {self.current_industry} industry."
        
        perspective_details = bsc_analysis["perspectives"][perspective]
        perspective_name = perspective.replace("_", " ").title()
        
        answer = f"# {perspective_name} for the {self.current_industry.title()} Industry\n\n"
        
        answer += "## Key Objectives\n"
        for objective in perspective_details["objectives"]:
            answer += f"- {objective}\n"
        
        answer += "\n## Key Metrics\n"
        for metric in perspective_details["metrics"]:
            answer += f"### {metric['metric']}\n"
            answer += f"Description: {metric['description']}\n"
            answer += f"Industry benchmark: {metric['industry_benchmark']}\n"
            answer += f"Process implications: {metric['process_implications']}\n\n"
        
        answer += "## Process Maturity Assessment\n"
        maturity = perspective_details["maturity_assessment"]
        answer += f"Current state: {maturity['current_state']}\n\n"
        
        answer += "Challenges:\n"
        for challenge in maturity["challenges"]:
            answer += f"- {challenge}\n"
        
        answer += "\nImprovement opportunities:\n"
        for opportunity in maturity["improvement_opportunities"]:
            answer += f"- {opportunity}\n"
        
        return answer
    
    def _answer_process_recommendations(self) -> str:
        """Answer questions about process optimization recommendations."""
        recommendations = self.get_process_optimization_recommendations()
        
        answer = f"# Process Optimization Recommendations for the {self.current_industry.title()} Industry\n\n"
        
        answer += "## Short-Term Improvements (0-6 months)\n\n"
        for rec in recommendations["short_term"]:
            answer += f"### {rec['area']}: {rec['recommendation']}\n"
            answer += f"{rec['description']}\n\n"
            
            answer += "Benefits:\n"
            for benefit in rec["benefits"]:
                answer += f"- {benefit}\n"
            
            answer += "\nImplementation approach:\n"
            for step in rec["implementation_approach"]:
                answer += f"- {step}\n"
            
            answer += "\nKey performance indicators:\n"
            for kpi in rec["key_performance_indicators"]:
                answer += f"- {kpi}\n"
            
            answer += "\n"
        
        answer += "## Medium-Term Transformations (6-18 months)\n\n"
        for rec in recommendations["medium_term"]:
            answer += f"### {rec['area']}: {rec['recommendation']}\n"
            answer += f"{rec['description']}\n\n"
            
            answer += "Benefits:\n"
            for benefit in rec["benefits"]:
                answer += f"- {benefit}\n"
            
            answer += "\nImplementation approach:\n"
            for step in rec["implementation_approach"]:
                answer += f"- {step}\n"
            
            answer += "\nKey performance indicators:\n"
            for kpi in rec["key_performance_indicators"]:
                answer += f"- {kpi}\n"
            
            answer += "\n"
        
        answer += "## Long-Term Strategic Innovations (18+ months)\n\n"
        for rec in recommendations["long_term"]:
            answer += f"### {rec['area']}: {rec['recommendation']}\n"
            answer += f"{rec['description']}\n\n"
            
            answer += "Benefits:\n"
            for benefit in rec["benefits"]:
                answer += f"- {benefit}\n"
            
            answer += "\nImplementation approach:\n"
            for step in rec["implementation_approach"]:
                answer += f"- {step}\n"
            
            answer += "\nKey performance indicators:\n"
            for kpi in rec["key_performance_indicators"]:
                answer += f"- {kpi}\n"
            
            answer += "\n"
        
        return answer
    
    def _answer_specific_recommendations(self, timeframe: str) -> str:
        """Answer questions about specific timeframe recommendations."""
        recommendations = self.get_process_optimization_recommendations()
        
        if timeframe not in recommendations:
            return f"I don't have {timeframe} recommendations for the {self.current_industry} industry."
        
        timeframe_display = {
            "short_term": "Short-Term Improvements (0-6 months)",
            "medium_term": "Medium-Term Transformations (6-18 months)",
            "long_term": "Long-Term Strategic Innovations (18+ months)"
        }
        
        answer = f"# {timeframe_display[timeframe]} for the {self.current_industry.title()} Industry\n\n"
        
        for rec in recommendations[timeframe]:
            answer += f"## {rec['area']}: {rec['recommendation']}\n"
            answer += f"{rec['description']}\n\n"
            
            answer += "Benefits:\n"
            for benefit in rec["benefits"]:
                answer += f"- {benefit}\n"
            
            answer += "\nImplementation approach:\n"
            for step in rec["implementation_approach"]:
                answer += f"- {step}\n"
            
            answer += "\nKey performance indicators:\n"
            for kpi in rec["key_performance_indicators"]:
                answer += f"- {kpi}\n"
            
            answer += "\n"
        
        return answer
    
    def _answer_value_chain(self) -> str:
        """Answer questions about value chain analysis."""
        value_chain = self.analyze_value_chain()
        
        answer = f"# Value Chain Analysis for the {self.current_industry.title()} Industry\n\n"
        answer += f"{value_chain['framework_description']}\n\n"
        
        for activity, details in value_chain["activities"].items():
            activity_name = activity.replace("_", " ").title()
            answer += f"## {activity_name}\n\n"
            
            # The structure varies by activity, so we need to handle different formats
            if isinstance(details, dict):
                for key, value in details.items():
                    if isinstance(value, list):
                        answer += f"### {key.replace('_', ' ').title()}\n"
                        for item in value:
                            if isinstance(item, dict) and "name" in item and "description" in item:
                                answer += f"- **{item['name']}**: {item['description']}\n"
                            else:
                                answer += f"- {item}\n"
                        answer += "\n"
                    elif isinstance(value, dict):
                        answer += f"### {key.replace('_', ' ').title()}\n"
                        for subkey, subvalue in value.items():
                            answer += f"#### {subkey.replace('_', ' ').title()}\n"
                            if isinstance(subvalue, list):
                                for item in subvalue:
                                    answer += f"- {item}\n"
                            else:
                                answer += f"{subvalue}\n"
                            answer += "\n"
                    else:
                        answer += f"### {key.replace('_', ' ').title()}\n"
                        answer += f"{value}\n\n"
            
            # Check if there are process implications
            if "process_implications" in details:
                answer += "### Process Implications\n"
                for implication in details["process_implications"]:
                    answer += f"- {implication}\n"
                answer += "\n"
        
        return answer
    
    def _answer_bpm_principles(self) -> str:
        """Answer questions about BPM principles."""
        principles = self.get_bpm_principles()
        
        answer = "# Core Business Process Management Principles\n\n"
        
        for principle in principles["core_principles"]:
            answer += f"## {principle['name']}\n"
            answer += f"{principle['description']}\n\n"
            
            answer += "Benefits:\n"
            for benefit in principle["benefits"]:
                answer += f"- {benefit}\n"
            
            answer += "\nImplementation strategies:\n"
            for strategy in principle["implementation_strategies"]:
                answer += f"- {strategy}\n"
            
            answer += "\n"
        
        return answer
    
    def _answer_bpm_methodologies(self) -> str:
        """Answer questions about BPM methodologies."""
        principles = self.get_bpm_principles()
        
        answer = "# Business Process Management Methodologies\n\n"
        
        for methodology in principles["methodologies"]:
            answer += f"## {methodology['name']}\n"
            answer += f"{methodology['description']}\n\n"
            
            answer += "Key concepts:\n"
            for concept in methodology["key_concepts"]:
                answer += f"- {concept}\n"
            
            answer += "\nTools:\n"
            for tool in methodology["tools"]:
                answer += f"- {tool}\n"
            
            if "types_of_waste" in methodology:
                answer += "\nTypes of waste:\n"
                for waste in methodology["types_of_waste"]:
                    answer += f"- {waste}\n"
            
            if "steps" in methodology:
                answer += "\nImplementation steps:\n"
                for step in methodology["steps"]:
                    answer += f"- {step}\n"
            
            answer += f"\nBPM application: {methodology['bpm_application']}\n\n"
        
        return answer
    
    def _answer_technology_enablers(self) -> str:
        """Answer questions about BPM technology enablers."""
        enablers = self.get_technology_enablers()
        
        answer = "# Business Process Management Technology Enablers\n\n"
        
        for enabler in enablers["enablers"]:
            answer += f"## {enabler['name']}\n"
            answer += f"{enabler['description']}\n\n"
            
            answer += "Capabilities:\n"
            for capability in enabler["capabilities"]:
                answer += f"- {capability}\n"
            
            answer += "\nExamples:\n"
            for example in enabler["examples"]:
                answer += f"- {example}\n"
            
            answer += "\n"
        
        return answer
    
    def _answer_performance_metrics(self) -> str:
        """Answer questions about BPM performance metrics."""
        metrics = self.get_bpm_performance_metrics()
        
        answer = "# Business Process Management Performance Metrics\n\n"
        
        for category in metrics["metrics_by_category"]:
            answer += f"## {category['category']} Metrics\n\n"
            
            for metric in category["metrics"]:
                answer += f"### {metric['name']}\n"
                answer += f"{metric['description']}\n"
                answer += f"Calculation: {metric['calculation']}\n\n"
                
                answer += "Improvement strategies:\n"
                for strategy in metric["improvement_strategies"]:
                    answer += f"- {strategy}\n"
                
                answer += "\n"
        
        return answer
    
    def _answer_implementation_practices(self) -> str:
        """Answer questions about BPM implementation practices."""
        practices = self.get_bpm_implementation_practices()
        
        answer = "# Business Process Management Implementation Best Practices\n\n"
        
        for phase in practices["best_practices"]:
            answer += f"## {phase['phase']}\n\n"
            
            for practice in phase["practices"]:
                answer += f"- {practice}\n"
            
            answer += "\n"
        
        return answer
    
    def _answer_bpm_challenges(self) -> str:
        """Answer questions about common BPM challenges."""
        practices = self.get_bpm_implementation_practices()
        
        answer = "# Common Challenges in Business Process Management\n\n"
        
        for challenge in practices["common_challenges"]:
            answer += f"## {challenge['challenge']}\n"
            answer += f"{challenge['description']}\n\n"
            
            answer += "Mitigation strategies:\n"
            for strategy in challenge["mitigation_strategies"]:
                answer += f"- {strategy}\n"
            
            answer += "\n"
        
        return answer
    
    def _load_json(self, filename: str) -> Dict[str, Any]:
        """
        Load JSON data from a file.
        
        Args:
            filename: Name of the JSON file to load
            
        Returns:
            Dictionary containing the JSON data
        """
        try:
            with open(os.path.join(self.data_dir, filename), 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            return {}
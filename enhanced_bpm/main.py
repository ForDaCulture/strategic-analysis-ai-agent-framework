"""
Enhanced BPM Analysis System - Main Application

This script runs the enhanced BPM analysis system with interactive querying capabilities.
"""

import os
import sys
import json
import time
from typing import Dict, List, Any, Optional, Tuple

# Add the parent directory to the path to import the models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from enhanced_bpm.models.bpm_analyzer import BPMAnalyzer

def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def print_section(title: str) -> None:
    """Print a formatted section title."""
    print("\n" + "-" * 80)
    print(f" {title} ".center(80, "-"))
    print("-" * 80 + "\n")

def print_subsection(title: str) -> None:
    """Print a formatted subsection title."""
    print(f"\n--- {title} ---\n")

def print_json(data: Dict[str, Any], indent: int = 2) -> None:
    """Print JSON data in a formatted way."""
    print(json.dumps(data, indent=indent))

def print_list(items: List[str], title: str = None) -> None:
    """Print a list of items with an optional title."""
    if title:
        print(f"\n{title}:")
    
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    
    print()

def get_user_choice(prompt: str, options: List[str], allow_custom: bool = False) -> str:
    """
    Get a choice from the user.
    
    Args:
        prompt: The prompt to display to the user
        options: List of options to choose from
        allow_custom: Whether to allow custom input
        
    Returns:
        The selected option or custom input
    """
    print(prompt)
    
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    if allow_custom:
        print(f"{len(options) + 1}. Enter custom input")
    
    while True:
        try:
            choice = input("\nEnter your choice (number): ")
            
            if choice.isdigit():
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(options):
                    return options[choice_num - 1]
                elif allow_custom and choice_num == len(options) + 1:
                    custom_input = input("Enter your custom input: ")
                    return custom_input
            
            print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")

def run_demo_analysis(analyzer: BPMAnalyzer, industry: str) -> None:
    """
    Run a comprehensive demo analysis for the specified industry.
    
    Args:
        analyzer: The BPM analyzer instance
        industry: The industry to analyze
    """
    print_header(f"BPM Analysis for the {industry} Industry")
    
    # Set the industry
    if not analyzer.set_current_industry(industry):
        print(f"Error: Industry '{industry}' not found.")
        return
    
    # Get industry overview
    print_section("Industry Overview")
    overview = analyzer.get_industry_overview()
    print(f"Industry: {overview['name']}")
    print(f"Description: {overview['description']}")
    print(f"Market Size: {overview['market_size']['global_value']} with {overview['market_size']['projected_growth']} growth")
    
    print_subsection("Key Segments")
    for segment in overview['key_segments']:
        print(f"- {segment['name']}: {segment['description']}")
        print(f"  Market share: {segment['market_share']}")
        print(f"  Growth rate: {segment['growth_rate']}")
    
    print_subsection("Industry Drivers")
    for driver in overview['drivers']:
        print(f"- {driver['factor']}: {driver['impact']}")
    
    print_subsection("Challenges")
    for challenge in overview['challenges']:
        print(f"- {challenge['challenge']}: {challenge['impact']}")
    
    # Porter's Five Forces Analysis
    print_section("Porter's Five Forces Analysis")
    porter = analyzer.analyze_porter_five_forces()
    
    for force, details in porter["forces"].items():
        force_name = force.replace("_", " ").title()
        print_subsection(force_name)
        print(f"Level: {details['level']}")
        
        print("\nKey Factors:")
        for factor in details["factors"]:
            print(f"- {factor['factor']}: {factor['impact']}")
        
        print("\nProcess Implications:")
        for implication in details["process_implications"]:
            print(f"- {implication}")
    
    # Balanced Scorecard Analysis
    print_section("Balanced Scorecard Analysis")
    bsc = analyzer.analyze_balanced_scorecard()
    
    for perspective, details in bsc["perspectives"].items():
        perspective_name = perspective.replace("_", " ").title()
        print_subsection(perspective_name)
        
        print("Key Objectives:")
        for objective in details["objectives"]:
            print(f"- {objective}")
        
        print("\nKey Metrics:")
        for metric in details["metrics"]:
            print(f"- {metric['metric']}: {metric['industry_benchmark']}")
        
        print("\nProcess Maturity:")
        maturity = details["maturity_assessment"]
        print(f"Current state: {maturity['current_state']}")
    
    # Process Optimization Recommendations
    print_section("Process Optimization Recommendations")
    recommendations = analyzer.get_process_optimization_recommendations()
    
    print_subsection("Short-Term Improvements (0-6 months)")
    for rec in recommendations["short_term"]:
        print(f"- {rec['area']}: {rec['recommendation']}")
    
    print_subsection("Medium-Term Transformations (6-18 months)")
    for rec in recommendations["medium_term"]:
        print(f"- {rec['area']}: {rec['recommendation']}")
    
    print_subsection("Long-Term Strategic Innovations (18+ months)")
    for rec in recommendations["long_term"]:
        print(f"- {rec['area']}: {rec['recommendation']}")
    
    # Value Chain Analysis
    print_section("Value Chain Analysis")
    value_chain = analyzer.analyze_value_chain()
    
    for activity, details in value_chain["activities"].items():
        activity_name = activity.replace("_", " ").title()
        print_subsection(activity_name)
        
        if isinstance(details, dict) and "key_processes" in details:
            print("Key Processes:")
            for process in details["key_processes"]:
                print(f"- {process['name']}")
        
        if isinstance(details, dict) and "process_implications" in details:
            print("\nProcess Implications:")
            for implication in details["process_implications"]:
                print(f"- {implication}")
    
    # Competitive Landscape
    print_section("Competitive Landscape")
    landscape = analyzer.get_competitive_landscape()
    
    print(f"Market Concentration: {landscape['market_concentration']}")
    
    print_subsection("Key Players")
    for player in landscape["key_players"]:
        print(f"- {player['name']} ({player['market_share']} market share)")
        print(f"  Headquarters: {player['headquarters']}")
        print("  Key strengths:")
        for strength in player["key_strengths"]:
            print(f"    - {strength}")
    
    print_subsection("New Entrants")
    for entrant in landscape["new_entrants"]:
        print(f"- {entrant['name']} (Focus: {entrant['focus']})")
    
    # Business Process Analysis
    print_section("Business Process Analysis")
    processes = analyzer.get_business_process_analysis()
    
    for area, details in processes.items():
        area_name = area.replace("_", " ").title()
        print_subsection(area_name)
        
        print(f"Maturity Level: {details['maturity_level']}")
        print(f"Automation Level: {details['automation_level']}")
        
        print("\nKey Processes:")
        for process in details["key_processes"]:
            print(f"- {process['name']}: {process['description']}")
        
        print("\nKey Challenges:")
        for challenge in details["key_challenges"]:
            print(f"- {challenge['challenge']}")

def interactive_mode(analyzer: BPMAnalyzer) -> None:
    """
    Run the BPM analyzer in interactive mode.
    
    Args:
        analyzer: The BPM analyzer instance
    """
    print_header("Enhanced BPM Analysis System - Interactive Mode")
    
    # Get available industries
    available_industries = analyzer.load_available_industries()
    
    if not available_industries:
        print("Error: No industry data files found.")
        return
    
    # Select an industry
    selected_industry = get_user_choice(
        "Select an industry to analyze:",
        available_industries
    )
    
    # Set the industry
    if not analyzer.set_current_industry(selected_industry):
        print(f"Error: Industry '{selected_industry}' not found.")
        return
    
    print(f"\nIndustry '{selected_industry}' selected.\n")
    
    # Main interaction loop
    while True:
        print_section("Available Actions")
        
        actions = [
            "Run comprehensive analysis",
            "View industry overview",
            "Analyze Porter's Five Forces",
            "Analyze Balanced Scorecard",
            "View process optimization recommendations",
            "Analyze value chain",
            "View competitive landscape",
            "View business process analysis",
            "Ask a specific question",
            "Change industry",
            "Exit"
        ]
        
        selected_action = get_user_choice(
            "What would you like to do?",
            actions
        )
        
        if selected_action == "Run comprehensive analysis":
            run_demo_analysis(analyzer, selected_industry)
        
        elif selected_action == "View industry overview":
            print_section("Industry Overview")
            overview = analyzer.get_industry_overview()
            print_json(overview)
        
        elif selected_action == "Analyze Porter's Five Forces":
            print_section("Porter's Five Forces Analysis")
            porter = analyzer.analyze_porter_five_forces()
            print_json(porter)
        
        elif selected_action == "Analyze Balanced Scorecard":
            print_section("Balanced Scorecard Analysis")
            bsc = analyzer.analyze_balanced_scorecard()
            print_json(bsc)
        
        elif selected_action == "View process optimization recommendations":
            print_section("Process Optimization Recommendations")
            recommendations = analyzer.get_process_optimization_recommendations()
            print_json(recommendations)
        
        elif selected_action == "Analyze value chain":
            print_section("Value Chain Analysis")
            value_chain = analyzer.analyze_value_chain()
            print_json(value_chain)
        
        elif selected_action == "View competitive landscape":
            print_section("Competitive Landscape")
            landscape = analyzer.get_competitive_landscape()
            print_json(landscape)
        
        elif selected_action == "View business process analysis":
            print_section("Business Process Analysis")
            processes = analyzer.get_business_process_analysis()
            print_json(processes)
        
        elif selected_action == "Ask a specific question":
            print_section("Ask a Question")
            print("You can ask questions about the industry, BPM principles, or specific analyses.")
            print("Examples:")
            print("- What are the key challenges in the industry?")
            print("- How strong is the bargaining power of suppliers?")
            print("- What are the recommended short-term process improvements?")
            print("- What are the core BPM principles?")
            
            question = input("\nEnter your question: ")
            
            print_section("Answer")
            answer = analyzer.answer_question(question)
            print(answer)
        
        elif selected_action == "Change industry":
            # Select a new industry
            selected_industry = get_user_choice(
                "Select an industry to analyze:",
                available_industries
            )
            
            # Set the industry
            if not analyzer.set_current_industry(selected_industry):
                print(f"Error: Industry '{selected_industry}' not found.")
                continue
            
            print(f"\nIndustry '{selected_industry}' selected.\n")
        
        elif selected_action == "Exit":
            print("\nThank you for using the Enhanced BPM Analysis System. Goodbye!")
            break
        
        # Pause before showing the menu again
        input("\nPress Enter to continue...")

def main() -> None:
    """Main function to run the BPM analysis system."""
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize the BPM analyzer
    analyzer = BPMAnalyzer(data_dir=data_dir)
    
    # Check if we have the required data files
    required_files = [
        "bpm_principles.json",
        "electric_vehicle_industry.json"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(data_dir, file)):
            missing_files.append(file)
    
    if missing_files:
        print("Error: The following required data files are missing:")
        for file in missing_files:
            print(f"- {file}")
        print("\nPlease make sure these files exist in the 'data' directory.")
        return
    
    # Run in interactive mode
    try:
        interactive_mode(analyzer)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
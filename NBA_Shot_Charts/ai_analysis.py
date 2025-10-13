import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def analyze_player_performance(player_name, season_id, player_stats, zone_stats, league_comparison):
    """
    Generate AI analysis of a player's performance for a specified season.
    
    Args:
        player_name: Player's full name
        season_id: Season identifier (e.g., "2022-23")
        player_stats: Dict with total_shots, made_shots, fg_percentage
        zone_stats: Dict with zone-by-zone statistics
        league_comparison: Dict with player vs league average by zone
    
    Returns:
        String containing the AI analysis
    """
    
    # Prepare zone statistics summary
    zone_summary = []
    for zone, stats in zone_stats.items():
        fg_pct = stats['FG_PCT'] * 100
        zone_summary.append(f"{zone}: {stats['FGM']}/{stats['FGA']} ({fg_pct:.1f}%)")
    
    # Prepare league comparison summary
    comparison_summary = []
    if league_comparison:
        for zone in league_comparison.get('categories', []):
            idx = league_comparison['categories'].index(zone)
            player_pct = league_comparison['player_values'][idx]
            league_pct = league_comparison['league_avg'][idx]
            diff = player_pct - league_pct
            comparison_summary.append(
                f"{zone}: Player {player_pct:.1f}% vs League {league_pct:.1f}% ({diff:+.1f}%)"
            )
    
    prompt = f"""You are an expert NBA analyst. Analyze the following shooting performance for {player_name} during the {season_id} season.

**Overall Statistics:**
- Total Shots Attempted: {player_stats['total_shots']}
- Shots Made: {player_stats['made_shots']}
- Field Goal Percentage: {player_stats['fg_percentage']}%

**Zone-by-Zone Performance:**
{chr(10).join(zone_summary)}

**Comparison to League Average:**
{chr(10).join(comparison_summary) if comparison_summary else 'League comparison data not available'}

Please provide a CONCISE analysis (100-150 words maximum) covering:

1. Overall shooting efficiency assessment (above/below league average)
2. Top 2 strengths (best performing zones)
3. Main weakness (lowest performing zone)
4. One key insight about their playing style

Be direct and analytical. Focus only on the most important findings."""

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        # Convert Markdown to HTML for better formatting
        html_content = markdown.markdown(response.text, extensions=['nl2br', 'tables'])
        return html_content
    except Exception as e:
        print(f"Error generating AI analysis: {e}")
        return "<p>AI analysis is currently unavailable. Please try again later.</p>"


def analyze_player_comparison(player1_name, player1_season, player1_stats, player1_zones,
                              player2_name, player2_season, player2_stats, player2_zones):
    """
    Generate AI analysis comparing two players' performances.
    
    Args:
        player1_name: First player's name
        player1_season: First player's season
        player1_stats: First player's overall stats dict
        player1_zones: First player's zone statistics dict
        player2_name: Second player's name
        player2_season: Second player's season
        player2_stats: Second player's overall stats dict
        player2_zones: Second player's zone statistics dict
    
    Returns:
        String containing the comparative AI analysis
    """
    
    # Prepare zone comparisons
    zone_comparisons = []
    all_zones = set(list(player1_zones.keys()) + list(player2_zones.keys()))
    
    for zone in sorted(all_zones):
        p1_stats = player1_zones.get(zone, {'FGM': 0, 'FGA': 0, 'FG_PCT': 0})
        p2_stats = player2_zones.get(zone, {'FGM': 0, 'FGA': 0, 'FG_PCT': 0})
        
        p1_pct = p1_stats['FG_PCT'] * 100
        p2_pct = p2_stats['FG_PCT'] * 100
        
        zone_comparisons.append(
            f"{zone}: {player1_name} {p1_pct:.1f}% ({p1_stats['FGM']}/{p1_stats['FGA']}) vs "
            f"{player2_name} {p2_pct:.1f}% ({p2_stats['FGM']}/{p2_stats['FGA']})"
        )
    
    prompt = f"""You are an expert NBA analyst making a definitive judgment call. Compare these two players:

**{player1_name} ({player1_season})**
- Total Shots: {player1_stats['total_shots']}
- Made Shots: {player1_stats['made_shots']}
- FG%: {player1_stats['fg_percentage']}%

**{player2_name} ({player2_season})**
- Total Shots: {player2_stats['total_shots']}
- Made Shots: {player2_stats['made_shots']}
- FG%: {player2_stats['fg_percentage']}%

**Zone-by-Zone Comparison:**
{chr(10).join(zone_comparisons)}

Provide a CONCISE, DEFINITIVE analysis (100-150 words maximum):

1. **THE VERDICT**: Start with "**{player1_name} is the better player**" OR "**{player2_name} is the better player**". Make a clear choice - do NOT say "more efficient" or "better shooter". Say who is THE BETTER PLAYER overall based on their shooting performance.

2. **WHY THEY'RE BETTER**: Give 2-3 concrete reasons with percentages. Consider: overall scoring efficiency, ability to score from multiple areas, volume, and impact on the game.

3. **THE KEY DIFFERENCE**: One sentence on what separates the winner from the loser.

Be bold and decisive. Pick a winner and defend it. No hedging, no "it depends", no "both are great in different ways". CHOOSE ONE."""

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        # Convert Markdown to HTML for better formatting
        html_content = markdown.markdown(response.text, extensions=['nl2br', 'tables'])
        return html_content
    except Exception as e:
        print(f"Error generating comparison analysis: {e}")
        return "<p>AI comparison analysis is currently unavailable. Please try again later.</p>"
from flask import Blueprint, render_template, request, jsonify
from . import data, plotting, ai_analysis

import pandas as pd

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@main_bp.route('/compare')
def compare():
    """Render the player comparison page."""
    return render_template('comparison.html')

@main_bp.route('/comparison-result', methods=['POST'])
def comparison_result():
    """Process comparison form submission and generate side-by-side shot charts."""
    try:
        player1_name = request.form.get('player1_name', '').strip()
        season1_id = request.form.get('season1_id', '').strip()
        player2_name = request.form.get('player2_name', '').strip()
        season2_id = request.form.get('season2_id', '').strip()

        if not all([player1_name, season1_id, player2_name, season2_id]):
            return render_template('comparison.html', error='Please provide both players and their seasons.')

        # Get player 1 info
        player1_info = data.find_player(player1_name)
        if not player1_info:
            return render_template('comparison.html', error=f"Player '{player1_name}' not found.")

        # Get player 2 info
        player2_info = data.find_player(player2_name)
        if not player2_info:
            return render_template('comparison.html', error=f"Player '{player2_name}' not found.")

        # Fetch shot data for both players
        shot1_df, _ = data.get_player_shotchartdetail(player1_info['id'], season1_id)
        shot2_df, _ = data.get_player_shotchartdetail(player2_info['id'], season2_id)

        if shot1_df.empty:
            return render_template('comparison.html', error=f'{player1_name} has no shot data for the {season1_id} season.')
        
        if shot2_df.empty:
            return render_template('comparison.html', error=f'{player2_name} has no shot data for the {season2_id} season.')
        
        # Generate shot charts with unique div IDs
        title1 = f"{player1_name} | {season1_id}"
        title2 = f"{player2_name} | {season2_id}"
        chart1_html = plotting.draw_plot(shot1_df, title1, div_id='shot-chart-1', include_plotlyjs='cdn')
        chart2_html = plotting.draw_plot(shot2_df, title2, div_id='shot-chart-2', include_plotlyjs=False)

        # Calculate overall stats for player 1
        total_shots1 = len(shot1_df)
        made_shots1 = shot1_df['SHOT_MADE_FLAG'].sum()
        fg_percentage1 = (made_shots1 / total_shots1 * 100) if total_shots1 > 0 else 0
        
        player1_stats = {
            'total_shots': total_shots1,
            'made_shots': made_shots1,
            'fg_percentage': round(fg_percentage1, 1)
        }

        # Calculate overall stats for player 2
        total_shots2 = len(shot2_df)
        made_shots2 = shot2_df['SHOT_MADE_FLAG'].sum()
        fg_percentage2 = (made_shots2 / total_shots2 * 100) if total_shots2 > 0 else 0
        
        player2_stats = {
            'total_shots': total_shots2,
            'made_shots': made_shots2,
            'fg_percentage': round(fg_percentage2, 1)
        }

        # Calculate zone stats for player 1
        zone_stats1 = shot1_df.groupby('SHOT_ZONE_RANGE')
        personal_zone_stats1 = pd.DataFrame({
            'FGM': zone_stats1['SHOT_MADE_FLAG'].sum(),
            'FGA': zone_stats1.size()
        }).reset_index()
        personal_zone_stats1['FG_PCT'] = (personal_zone_stats1['FGM'] / personal_zone_stats1['FGA']).fillna(0)
        
        # Calculate zone stats for player 2
        zone_stats2 = shot2_df.groupby('SHOT_ZONE_RANGE')
        personal_zone_stats2 = pd.DataFrame({
            'FGM': zone_stats2['SHOT_MADE_FLAG'].sum(),
            'FGA': zone_stats2.size()
        }).reset_index()
        personal_zone_stats2['FG_PCT'] = (personal_zone_stats2['FGM'] / personal_zone_stats2['FGA']).fillna(0)
        
        zone_order = [
            'Less Than 8 ft.',
            '8-16 ft.',
            '16-24 ft.',
            '24+ ft.',
            'Back Court Shot'
        ]
        
        # Convert to dictionaries for template
        player1_zone_stats = personal_zone_stats1.set_index('SHOT_ZONE_RANGE').to_dict('index')
        player2_zone_stats = personal_zone_stats2.set_index('SHOT_ZONE_RANGE').to_dict('index')

        # Prepare chart data
        player1_chart_data = []
        player2_chart_data = []
        
        for zone in zone_order:
            player1_chart_data.append(
                player1_zone_stats[zone]['FG_PCT'] * 100 if zone in player1_zone_stats else 0
            )
            player2_chart_data.append(
                player2_zone_stats[zone]['FG_PCT'] * 100 if zone in player2_zone_stats else 0
            )

        # Generate AI comparison analysis
        ai_comparison = ai_analysis.analyze_player_comparison(
            player1_name, season1_id, player1_stats, player1_zone_stats,
            player2_name, season2_id, player2_stats, player2_zone_stats
        )

        return render_template('comparison_result.html',
                               player1_name=player1_name,
                               player2_name=player2_name,
                               season1_id=season1_id,
                               season2_id=season2_id,
                               chart1_html=chart1_html,
                               chart2_html=chart2_html,
                               player1_stats=player1_stats,
                               player2_stats=player2_stats,
                               player1_zone_stats=player1_zone_stats,
                               player2_zone_stats=player2_zone_stats,
                               zone_order=zone_order,
                               player1_chart_data=player1_chart_data,
                               player2_chart_data=player2_chart_data,
                               ai_comparison=ai_comparison)

    except ValueError as ve:
        return render_template('comparison.html', error=str(ve))
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 
        return render_template('comparison.html', error='An unexpected error occurred. Please try again.')

@main_bp.route('/result', methods=['POST'])
def result():
    """Process form submission and generate shot chart."""
    try:
        player_name = request.form.get('player_name', '').strip()
        season_id = request.form.get('season_id', '').strip()

        if not player_name or not season_id:
            return render_template('index.html', error='Please provide both a player and a season.')

        player_info = data.find_player(player_name)
        if not player_info:
            return render_template('index.html', error=f"Player '{player_name}' not found.")

        shot_df, league_avg_df = data.get_player_shotchartdetail(player_info['id'], season_id)

        if shot_df.empty:
            return render_template('index.html', error=f'{player_name} has no shot data for the {season_id} season.')
        
        title = f"{player_name} | {season_id} Regular Season"
        chart_html = plotting.draw_plot(shot_df, title)

        total_shots = len(shot_df)
        made_shots = shot_df['SHOT_MADE_FLAG'].sum()
        fg_percentage = (made_shots / total_shots * 100) if total_shots > 0 else 0
        
        player_stats = {
            'total_shots': total_shots,
            'made_shots': made_shots,
            'fg_percentage': round(fg_percentage, 1)
        }

        zone_stats = shot_df.groupby('SHOT_ZONE_RANGE')
        personal_zone_stats = pd.DataFrame({
            'FGM': zone_stats['SHOT_MADE_FLAG'].sum(),
            'FGA': zone_stats.size()
        }).reset_index()
        personal_zone_stats['FG_PCT'] = (personal_zone_stats['FGM'] / personal_zone_stats['FGA']).fillna(0)
        
        zone_order = [
            'Less Than 8 ft.',
            '8-16 ft.',
            '16-24 ft.',
            '24+ ft.',
            'Back Court Shot'
        ]
        
        personal_zone_stats['SHOT_ZONE_RANGE'] = pd.Categorical(
            personal_zone_stats['SHOT_ZONE_RANGE'],
            categories=zone_order,
            ordered=True
        )

        personal_zone_stats = personal_zone_stats.sort_values('SHOT_ZONE_RANGE')
        personal_stats_by_zone = personal_zone_stats.set_index('SHOT_ZONE_RANGE').to_dict('index')

        # Prepare league comparison data for AI analysis
        league_comparison = None
        try:
            # Calculate player stats by zone
            player_zone_stats = shot_df.groupby('SHOT_ZONE_RANGE').agg({
                'SHOT_MADE_FLAG': ['sum', 'count']
            }).reset_index()
            player_zone_stats.columns = ['SHOT_ZONE_RANGE', 'FGM', 'FGA']
            player_zone_stats['FG_PCT'] = (player_zone_stats['FGM'] / player_zone_stats['FGA'] * 100).round(1)
            
            # Calculate league average by zone
            league_zone_stats = league_avg_df.groupby('SHOT_ZONE_RANGE').agg({
                'FGM': 'sum',
                'FGA': 'sum'
            }).reset_index()
            league_zone_stats['FG_PCT'] = (league_zone_stats['FGM'] / league_zone_stats['FGA'] * 100).round(1)
            
            categories = []
            player_values = []
            league_values = []
            
            for zone in zone_order:
                player_row = player_zone_stats[player_zone_stats['SHOT_ZONE_RANGE'] == zone]
                league_row = league_zone_stats[league_zone_stats['SHOT_ZONE_RANGE'] == zone]
                
                if not player_row.empty:
                    categories.append(zone)
                    player_values.append(float(player_row['FG_PCT'].iloc[0]))
                    league_values.append(float(league_row['FG_PCT'].iloc[0]) if not league_row.empty else 0)
            
            league_comparison = {
                'categories': categories,
                'player_values': player_values,
                'league_avg': league_values
            }
        except Exception as e:
            print(f"Error preparing league comparison: {e}")

        # Generate AI analysis
        ai_report = ai_analysis.analyze_player_performance(
            player_name, 
            season_id, 
            player_stats, 
            personal_stats_by_zone,
            league_comparison
        )

        return render_template('result.html',
                               title=title,
                               chart_html=chart_html,
                               player_stats=player_stats,
                               personal_stats_by_zone=personal_stats_by_zone,
                               player_id=player_info['id'],
                               season_id=season_id,
                               ai_analysis=ai_report)

    except ValueError as ve:
        return render_template('index.html', error=str(ve))
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 
        return render_template('index.html', error='An unexpected error occurred. Please try again.')


@main_bp.route('/api/player-comparison/<int:player_id>/<season_id>')
def api_player_comparison(player_id, season_id):
    """Get player stats compared to league average for a specific season."""
    try:
        shot_df, league_avg_df = data.get_player_shotchartdetail(player_id, season_id)
        
        if shot_df.empty or league_avg_df.empty:
            return jsonify({"error": "No data available"}), 404
        
        # Calculate player stats by zone
        player_zone_stats = shot_df.groupby('SHOT_ZONE_RANGE').agg({
            'SHOT_MADE_FLAG': ['sum', 'count']
        }).reset_index()
        player_zone_stats.columns = ['SHOT_ZONE_RANGE', 'FGM', 'FGA']
        player_zone_stats['FG_PCT'] = (player_zone_stats['FGM'] / player_zone_stats['FGA'] * 100).round(1)
        
        # Calculate league average by zone
        league_zone_stats = league_avg_df.groupby('SHOT_ZONE_RANGE').agg({
            'FGM': 'sum',
            'FGA': 'sum'
        }).reset_index()
        league_zone_stats['FG_PCT'] = (league_zone_stats['FGM'] / league_zone_stats['FGA'] * 100).round(1)
        
        # Merge and prepare data for chart
        zone_order = [
            'Less Than 8 ft.',
            '8-16 ft.',
            '16-24 ft.',
            '24+ ft.',
            'Back Court Shot'
        ]
        
        categories = []
        player_values = []
        league_values = []
        
        for zone in zone_order:
            player_row = player_zone_stats[player_zone_stats['SHOT_ZONE_RANGE'] == zone]
            league_row = league_zone_stats[league_zone_stats['SHOT_ZONE_RANGE'] == zone]
            
            if not player_row.empty:
                categories.append(zone)
                player_values.append(float(player_row['FG_PCT'].iloc[0]))
                league_values.append(float(league_row['FG_PCT'].iloc[0]) if not league_row.empty else 0)
        
        return jsonify({
            'categories': categories,
            'player_values': player_values,
            'league_avg': league_values
        })
        
    except Exception as e:
        print(f"Error in player comparison: {e}")
        return jsonify({"error": str(e)}), 500


@main_bp.route('/api/players')
def api_players():
    players_list = data.get_all_players()
    return jsonify([{'id': p['id'], 'name': p['full_name']} for p in players_list])

@main_bp.route('/api/player/<int:player_id>/seasons')
def api_player_seasons(player_id):
    try:
        seasons = data.get_player_career_seasons(player_id)
        return jsonify(seasons)
    except Exception:
        return jsonify({"error": "Could not fetch seasons for player"}), 500
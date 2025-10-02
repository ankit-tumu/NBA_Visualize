from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail, playercareerstats

# --- Caching ---
# Fetch the player list once when the module is first imported
print("Fetching and caching player data...")
_all_players = players.get_players()
_player_name_map = {player['full_name'].lower(): player for player in _all_players}
print("Player data cached.")

def get_all_players():
    """Returns the cached list of all NBA players."""
    return _all_players

def find_player(player_name):
    """
    Finds a player by full name from the cached list.
    
    Returns:
        dict: Player dictionary or None if not found.
    """
    return _player_name_map.get(player_name.lower())

def get_player_career_seasons(player_id):
    """
    Fetches the career statistics for a player and returns a list of seasons they played.
    """
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    # Return a sorted list of unique season IDs
    return sorted(career_df['SEASON_ID'].unique().tolist(), reverse=True)

def get_player_shotchartdetail(player_id, season_id):
    """
    Fetch shot chart data for a specific player and season.
    """
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]

    season_data = career_df[career_df['SEASON_ID'] == season_id]
    if season_data.empty:
        raise ValueError(f"Player did not play in the {season_id} season")

    team_id = season_data.iloc[0]['TEAM_ID']

    shotchartlist = shotchartdetail.ShotChartDetail(
        team_id=int(team_id),
        player_id=int(player_id),
        season_type_all_star='Regular Season',
        season_nullable=season_id,
        context_measure_simple='FGA'
    ).get_data_frames()

    return shotchartlist[0], shotchartlist[1]
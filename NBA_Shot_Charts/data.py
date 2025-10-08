from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail, playercareerstats

# --- Constants ---
EARLIEST_SEASON_YEAR = 2000  # Only show seasons from 2000 onwards

# --- Caching ---
# Fetch the player list once when the module is first imported
print("Fetching and caching player data...")
_all_players = players.get_players()
_player_name_map = {player['full_name'].lower(): player for player in _all_players}
print("Player data cached.")

def _season_year_from_id(season_id):
    """
    Extract the starting year from a season ID.
    Example: '2022-23' returns 2022, '1999-00' returns 1999
    """
    try:
        return int(season_id.split('-')[0])
    except (ValueError, IndexError):
        return 0

def get_all_players():
    """
    Returns the cached list of all NBA players.
    Note: Seasons will be filtered to only show 2000 onwards when a player is selected.
    """
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
    Only returns seasons from 2000 onwards.
    """
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    
    # Filter seasons to only include 2000 onwards
    all_seasons = career_df['SEASON_ID'].unique().tolist()
    filtered_seasons = [
        season for season in all_seasons 
        if _season_year_from_id(season) >= EARLIEST_SEASON_YEAR
    ]
    
    # Return a sorted list (most recent first)
    return sorted(filtered_seasons, reverse=True)

def get_player_shotchartdetail(player_id, season_id):
    """
    Fetch shot chart data for a specific player and season.
    Only allows seasons from 2000 onwards.
    """
    # Validate season year
    season_year = _season_year_from_id(season_id)
    if season_year < EARLIEST_SEASON_YEAR:
        raise ValueError(f"Season {season_id} is before {EARLIEST_SEASON_YEAR}. Only seasons from {EARLIEST_SEASON_YEAR} onwards are supported.")
    
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
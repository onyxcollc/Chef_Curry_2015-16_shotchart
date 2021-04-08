import numpy as np
import pandas as pd

#nba_api
from nba_api.stats.static import players 
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats


# matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch


# get_player_shotchartdetail: player_name, season_id -> player_shotchart_df, league_avg 

def get_player_shotchartdetail(player_name, season_id):
    
    # player dictionary 
    nba_players = players.get_players()
    player_dict = [ player for player in nba_players if player ['full_name'] == player_name][0]
    
    
    #career dataframe
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]
   
    
    # team id during the season
    team_id =career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']
    
    
    #shotchartdetail endpoints
    shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id),
                                                   player_id=int(player_dict['id']),
                                                   season_type_all_star='Regular Season',
                                                   season_nullable=season_id,
                                                   context_measure_simple="FGA").get_data_frames()
    
    return shotchartlist[0], shotchartlist[1]

 
   
 # draw court function
    
def draw_court(ax=None,color="blue", lw=1, outer_lines=False):
    
    if ax is None:
        ax = plt.gca()
    
   
    # Basketball Hoop
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)
    
    # Backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)
    
    # The Paint
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
    
    # Free Throw Top Arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    
    # Free Throw Bottom Arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2= 0, linewidth=lw, color=color)
    
    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    
    # Three Point Line
    corner_three_a = Rectangle((-220,-47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220,-47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0,0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
    
    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
    
    
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted, corner_three_b, corner_three_a, three_arc, center_outer_arc, center_inner_arc]
    

    if outer_lines:
        
        outer_lines = Rectangle((-250, -47.5), 500, 470, linwidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)
    
    
    
    
    for element in court_elements:
       
        ax.add_patch(element)

    # Shot Chart Function
     def shot_chart(data,title="", color="b", xlm=(-250, 250), ylim=(422.5, -47.5), line_color="blue",
                    court_color="white",court_lw=2, outer_lines=False,
                    flip_court=False, gridsize=None,
                    ax=None, despine=False):
            if (ax is None):
                ax = plt.gac()
                
            if not flip_court:
                ax.setxlim(xlim)
                ax.setylim(ylim)
            else:
                ax.set_xlim(xlim[::-1])
                ax.set_ylim(ylim[::-1])
                
            ax.tick_params(labelbottom="off", labeleft="off")
            ax.setitle(title, fontsize=18)
            
            # draw the court using the court 
            draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)
            
            # seperate color by make or miss
            
            x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
            y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']
            
            x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
            y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']
            
            # Plot missed shots 
            ax,scatter(x_missed,y_missed, c='r', marker="x", s=300, linewidth=3)
            
            # Plot made shots
            ax.scatter(x_made,y_made, facecolors='none',edgecolors='g', marker='o', s=100, linewidths=3)
            
            
            # Set the spines to match the rest of the court lines, makes outer_lines
            # somewhat unecessery 
            
            for spine in ax.spines:
                ax.spines[spine].set_lw(court_lw)
                ax.spines[spine].set_color(line_color)
                
            if despine:
                ax.spines["top"].set_visible(False) 
                ax.spines["bottom"].set_visible(False)  
                ax.spines["right"].set_visible(False)  
                ax.spines["left"].set_visible(False)  

            return ax







    
    
    
if __name__ == "__main__":
    
    get_player_shotchartdetail("LeBron James", "2019-20") 
    
    #print(player_shortchart_df)
    #print(league_avg)
    
    xlim = (-250, 250)
    ylim = (422.5, -47.5)
    
    ax = plt.gca()
    ax.set_xlim(xlim[::-1])
    ax.set_ylim(ylim[::-1])
    draw_court(ax)
    plt.show()
    
    
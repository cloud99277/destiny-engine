import argparse
import json
import hashlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime
import numpy as np
import os

def generate_candlesticks(start_year, dayuns, bazi_str):
    seed = int(hashlib.md5(bazi_str.encode('utf-8')).hexdigest(), 16) % 10000
    np.random.seed(seed)
    
    years = []
    opens, highs, lows, closes = [], [], [], []
    
    current_price = 50.0 
    
    for i in range(80): 
        current_year = start_year + i
        years.append(current_year)
        
        dayun_index = 0
        for idx, d in enumerate(dayuns):
            if current_year >= d.get('year', 0):
                dayun_index = idx
                
        d_gz = dayuns[dayun_index].get('ganzhi', '')
        d_hash = int(hashlib.md5(d_gz.encode()).hexdigest(), 16) % 100 if d_gz else 50
        d_momentum = (d_hash / 20.0) - 2.5 
            
        y_noise = np.random.normal(0, 6)
        
        open_price = current_price
        close_price = current_price + d_momentum + y_noise
        
        if close_price > 98: close_price = 98 - np.random.random()*5
        if close_price < 10: close_price = 10 + np.random.random()*5
        
        high_price = max(open_price, close_price) + abs(np.random.normal(0, 3))
        low_price = min(open_price, close_price) - abs(np.random.normal(0, 3))
        
        opens.append(open_price)
        highs.append(high_price)
        lows.append(low_price)
        closes.append(close_price)
        
        current_price = close_price
        
    return years, opens, highs, lows, closes

def plot_k_line(years, opens, highs, lows, closes, output_path):
    # Use default font but enable emoji via fallback if possible, or just skip CJK if font fails.
    # To avoid font crash, we use generic sans-serif for now, relying on matplotlib's internal fallback.
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    
    color_up = '#00ff9d'
    color_down = '#ff4d4d'
    
    for i in range(len(years)):
        if closes[i] >= opens[i]:
            color = color_up
            lower = opens[i]
            height = closes[i] - opens[i]
        else:
            color = color_down
            lower = closes[i]
            height = opens[i] - closes[i]
            
        ax.plot([years[i], years[i]], [lows[i], highs[i]], color=color, linewidth=1.5)
        ax.add_patch(Rectangle((years[i]-0.4, lower), 0.8, height, facecolor=color, edgecolor=color))
        
        vol_height = abs(closes[i] - opens[i]) + abs(highs[i] - lows[i])
        ax.bar(years[i], vol_height, width=0.8, bottom=0, color=color, alpha=0.3)

    ax.set_ylim(0, 110)
    ax.set_xlim(years[0]-1, years[-1]+1)
    
    ax.text(years[0], 102, "Cyber Destiny: 100-Year Karma K-Line", 
            color='white', fontsize=18, fontweight='bold')
            
    max_idx = np.argmax(highs)
    min_idx = np.argmin(lows)
    
    drops = [opens[i] - closes[i] for i in range(len(closes))]
    worst_drop_idx = np.argmax(drops)
    
    gains = [closes[i] - opens[i] for i in range(len(closes))]
    best_gain_idx = np.argmax(gains)

    ax.annotate('[God of Wealth]', 
                xy=(years[max_idx], highs[max_idx]), xytext=(-30, 25),
                textcoords='offset points', color='#00ff9d', fontsize=11,
                arrowprops=dict(arrowstyle="->", color='#00ff9d', connectionstyle="arc3,rad=.2"))
                
    ax.annotate('[Mercury Retrograde / Doom]', 
                xy=(years[min_idx], lows[min_idx]), xytext=(-40, -40),
                textcoords='offset points', color='#ff4d4d', fontsize=11,
                arrowprops=dict(arrowstyle="->", color='#ff4d4d', connectionstyle="arc3,rad=-.2"))
                
    ax.annotate('[Crazy Wage Slave]', 
                xy=(years[worst_drop_idx], highs[worst_drop_idx]), xytext=(20, 20),
                textcoords='offset points', color='yellow', fontsize=11,
                arrowprops=dict(arrowstyle="->", color='yellow'))
                
    ax.annotate('[Take-off / Windfall]', 
                xy=(years[best_gain_idx], lows[best_gain_idx]), xytext=(-50, -35),
                textcoords='offset points', color='#00aaff', fontsize=11,
                arrowprops=dict(arrowstyle="->", color='#00aaff'))

    ax.grid(True, linestyle='--', alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#30363d')
    ax.spines['bottom'].set_color('#30363d')
    ax.tick_params(colors='gray')
    
    ax.set_ylabel("Karma Index (0-100)", color='gray')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0d1117')
    print(f"K-Line chart saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    parser.add_argument("--out", default="life_k_line_v2.png")
    args = parser.parse_args()
    
    with open(args.json, 'r') as f:
        data = json.load(f)
        
    bazi_data = data.get('eastern_bazi', {})
    dayuns = bazi_data.get('dayuns', [])
    bazi_dict = bazi_data.get('bazi', {})
    bazi_str = f"{bazi_dict.get('year')}{bazi_dict.get('month')}{bazi_dict.get('day')}{bazi_dict.get('time')}"
    
    start_year = dayuns[0].get('year', 2000) if dayuns else 2000
        
    years, opens, highs, lows, closes = generate_candlesticks(start_year, dayuns, bazi_str)
    plot_k_line(years, opens, highs, lows, closes, args.out)

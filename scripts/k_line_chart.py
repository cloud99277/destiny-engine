import argparse
import json
import hashlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import os

def generate_trend(start_year, dayuns, bazi_str):
    # Deterministic noise based on bazi
    seed = int(hashlib.md5(bazi_str.encode('utf-8')).hexdigest(), 16) % 10000
    np.random.seed(seed)
    
    years = []
    prices = []
    
    # Starting base score
    current_price = 50.0 
    
    # Create 100 years of data
    for i in range(100):
        current_year = start_year + i
        years.append(datetime(current_year, 6, 1))
        
        # Check which dayun we are in
        dayun_index = 0
        for idx, d in enumerate(dayuns):
            if current_year >= d.get('year', 0):
                dayun_index = idx
                
        # Dayun momentum (-2 to 3) based on hash of the ganzhi
        d_gz = dayuns[dayun_index].get('ganzhi', '')
        if not d_gz:
            d_momentum = 0
        else:
            d_hash = int(hashlib.md5(d_gz.encode()).hexdigest(), 16) % 100
            d_momentum = (d_hash / 20.0) - 2.5 # -2.5 to +2.5
            
        # Yearly noise (LiuNian effect)
        y_noise = np.random.normal(0, 5)
        
        # Trend combination
        current_price += d_momentum + y_noise
        
        # Normalize bounds
        if current_price > 95: current_price = 95 - np.random.random()*5
        if current_price < 10: current_price = 10 + np.random.random()*5
        
        prices.append(current_price)
        
    return years, prices

def plot_k_line(years, prices, output_path):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    
    # Plot line
    ax.plot(years, prices, color='#00ff9d', linewidth=2)
    
    # Fill under line
    ax.fill_between(years, prices, 0, color='#00ff9d', alpha=0.1)
    
    # Add trend zones (Red for down, Green for up)
    for i in range(1, len(prices)):
        color = '#00ff9d' if prices[i] >= prices[i-1] else '#ff4d4d'
        ax.plot(years[i-1:i+1], prices[i-1:i+1], color=color, linewidth=2.5)
        
        # Draw volume-like bars at the bottom
        bar_height = abs(prices[i] - prices[i-1]) * 2
        ax.bar(years[i], bar_height, width=200, bottom=0, color=color, alpha=0.5)

    # Styling
    ax.set_ylim(0, 100)
    ax.set_title("100-Year Destiny Trend (K-Line Projection)", color='white', fontsize=16, pad=20)
    ax.set_ylabel("Destiny Momentum Index", color='gray')
    
    # Grid
    ax.grid(True, linestyle='--', alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#30363d')
    ax.spines['bottom'].set_color('#30363d')
    
    # Annotate Highest and Lowest points
    max_idx = np.argmax(prices)
    min_idx = np.argmin(prices)
    
    ax.annotate('Golden Era', xy=(years[max_idx], prices[max_idx]), xytext=(10, 10),
                textcoords='offset points', color='#00ff9d', fontweight='bold',
                arrowprops=dict(arrowstyle="->", color='#00ff9d'))
                
    ax.annotate('Pressure Test', xy=(years[min_idx], prices[min_idx]), xytext=(10, -20),
                textcoords='offset points', color='#ff4d4d', fontweight='bold',
                arrowprops=dict(arrowstyle="->", color='#ff4d4d'))

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0d1117')
    print(f"K-Line chart saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, help="Path to destiny_calc.json output")
    parser.add_argument("--out", default="life_k_line.png", help="Output image path")
    args = parser.parse_args()
    
    with open(args.json, 'r') as f:
        data = json.load(f)
        
    bazi_data = data.get('eastern_bazi', {})
    dayuns = bazi_data.get('dayuns', [])
    bazi_dict = bazi_data.get('bazi', {})
    bazi_str = f"{bazi_dict.get('year')}{bazi_dict.get('month')}{bazi_dict.get('day')}{bazi_dict.get('time')}"
    
    if not dayuns:
        # mock dayuns if not exist
        start_year = 2000
    else:
        start_year = dayuns[0].get('year', 2000)
        
    years, prices = generate_trend(start_year, dayuns, bazi_str)
    plot_k_line(years, prices, args.out)

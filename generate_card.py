#!/usr/bin/env python3
"""
Generate a dynamic card.svg with auto-updating age and GitHub stats
"""

from datetime import datetime, date
import urllib.request
import json
import os

# Set your birthdate here (YYYY, MM, DD)
BIRTHDATE = date(2001, 11, 1)  # November 1, 2001
GITHUB_USERNAME = "MinhajShafin"

def calculate_age():
    """Calculate age in years, months, and days"""
    today = date.today()

    years = today.year - BIRTHDATE.year
    months = today.month - BIRTHDATE.month
    days = today.day - BIRTHDATE.day

    # Adjust for negative days
    if days < 0:
        months -= 1
        # Get days in previous month
        if today.month == 1:
            prev_month = 12
            prev_year = today.year - 1
        else:
            prev_month = today.month - 1
            prev_year = today.year

        # Calculate days in previous month
        if prev_month in [1, 3, 5, 7, 8, 10, 12]:
            days_in_prev_month = 31
        elif prev_month in [4, 6, 9, 11]:
            days_in_prev_month = 30
        else:  # February
            if prev_year % 4 == 0 and (prev_year % 100 != 0 or prev_year % 400 == 0):
                days_in_prev_month = 29
            else:
                days_in_prev_month = 28

        days += days_in_prev_month

    # Adjust for negative months
    if months < 0:
        years -= 1
        months += 12

    return years, months, days

def fetch_github_stats():
    """Fetch GitHub statistics using GitHub API"""
    try:
        # Get GitHub token from environment variable (optional but recommended to avoid rate limits)
        token = os.environ.get('GITHUB_TOKEN', '')
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        if token:
            headers['Authorization'] = f'token {token}'

        # Fetch user data
        user_req = urllib.request.Request(
            f'https://api.github.com/users/{GITHUB_USERNAME}',
            headers=headers
        )
        with urllib.request.urlopen(user_req) as response:
            user_data = json.loads(response.read().decode())

        # Fetch repositories
        repos_req = urllib.request.Request(
            f'https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100',
            headers=headers
        )
        with urllib.request.urlopen(repos_req) as response:
            repos_data = json.loads(response.read().decode())

        # Calculate stats
        total_repos = user_data.get('public_repos', 0)
        followers = user_data.get('followers', 0)

        # Count stars across all repos
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)

        # Count contributed repos (repos you don't own but contributed to)
        contributed_repos = sum(1 for repo in repos_data if repo.get('fork', False))

        # Fetch commit count (approximation using events API)
        events_req = urllib.request.Request(
            f'https://api.github.com/users/{GITHUB_USERNAME}/events/public?per_page=100',
            headers=headers
        )
        try:
            with urllib.request.urlopen(events_req) as response:
                events_data = json.loads(response.read().decode())
            commit_count = sum(1 for event in events_data if event.get('type') == 'PushEvent')
            # This is an approximation - for accurate count, you'd need to iterate through all repos
            # For now, we'll use a placeholder or fetch from a more detailed source
            commit_count = max(commit_count, 57)  # Use at least the current count
        except:
            commit_count = 57  # Fallback to current value

        # Calculate lines of code (this is complex and requires analyzing all repos)
        # For now, we'll keep the current values as placeholders
        loc_total = 446
        loc_add = 3
        loc_del = 76

        return {
            'repos': str(total_repos).zfill(2),
            'contributed': str(contributed_repos),
            'stars': str(total_stars),
            'commits': str(commit_count),
            'followers': str(followers).zfill(2),
            'loc_total': str(loc_total),
            'loc_add': str(loc_add),
            'loc_del': str(loc_del)
        }

    except Exception as e:
        print(f"⚠️  Warning: Could not fetch GitHub stats: {e}")
        print("Using fallback values...")
        # Return fallback values if API fails
        return {
            'repos': '07',
            'contributed': 'X',
            'stars': 'X',
            'commits': '57',
            'followers': '03',
            'loc_total': '446',
            'loc_add': '3',
            'loc_del': '76'
        }

def calculate_dots(key_length, value_length, total_space=50):
    """Calculate the number of dots needed for spacing"""
    dots_count = total_space - key_length - value_length
    return " " + "." * max(dots_count, 1) + " "

def generate_card_svg():
    """Generate the card.svg with dynamic age and GitHub stats"""
    years, months, days = calculate_age()
    age_string = f"{years} years, {months} months, {days} days"

    # Fetch GitHub stats
    stats = fetch_github_stats()

    # Calculate dots for proper spacing
    age_dots_count = 22 - len(age_string)
    age_dots = " " + "." * age_dots_count + " "

    # Calculate dots for GitHub stats
    repo_dots = " " + "." * 4 + " "
    star_dots = " " + "." * (11 - len(stats['stars'])) + " "
    commit_dots = " " + "." * (17 - len(stats['commits'])) + " "
    follower_dots = " " + "." * 7 + " "
    loc_dots = "."

    svg_content = f'''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: #ffa657;}}
.value {{fill: #a5d6ff;}}
.addColor {{fill: #3fb950;}}
.delColor {{fill: #f85149;}}
.cc {{fill: #616e7f;}}
text, tspan {{white-space: pre;}}
</style>
<rect width="985px" height="530px" fill="#161b22" rx="15"/>
<text x="15" y="30" fill="#c9d1d9" class="ascii">
<tspan x="15" y="30">⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿</tspan>
<tspan x="15" y="50">⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿</tspan>
<tspan x="15" y="72">⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠟⠀⠀⠀⠸⠛⠛⠿⣿⣿⣿⣿⣿⣿</tspan>
<tspan x="15" y="94">⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⠛⠛⠛⠀⠀⠀⠀⠀⠘⠗⠀⠹⣿⣿⣿⣿⣿⣿⣿</tspan>
<tspan x="15" y="116">⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿</tspan>
<tspan x="15" y="138">⣿⣿⣿⣿⣿⠿⠟⠁⠀⠀⠀⠀⢀⣀⣠⡀⠀⠇⠁⠀⡀⠀⠀⠀⠈⡙⢿⣿⣿⣿</tspan>
<tspan x="15" y="160">⣿⡿⠟⠁⠀⠀⠀⠘⢶⠛⢑⡾⣿⣿⣿⣿⡀⠀⠂⠀⠀⠀⠀⠀⠄⣌⣈⠿⣿⣿ </tspan>
<tspan x="15" y="182">⡏⠀⠀⠀⠀⠀⠀⠀⠀⢰⣦⣱⣼⣿⣿⣿⣿⣷⣦⣄⢀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿ </tspan>
<tspan x="15" y="204">⣇⠀⠀⡀⠀⠀⠀⠀⠀⠘⠛⠋⠛⠛⠛⠻⣿⡿⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⣿⣿ </tspan>
<tspan x="15" y="226">⠇⠀⠹⢿⢸⣶⡀⠀⠄⠀⠀⠀⠀⠀⣄⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿ </tspan>
<tspan x="15" y="248">⣶⡄⠀⠀⠈⣿⢣⣾⣿⣯⣤⠀⠀⠀⣸⢀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿ </tspan>
<tspan x="15" y="270">⣿⣷⠀⠀⠀⠘⢸⡽⣿⣿⣿⣦⣦⣾⢇⣾⣿⣧⠀⠀⠀⡀⠀⡀⠀⠀⠀⠀⠀⢨⣿ </tspan>
<tspan x="15" y="292">⣿⣿⣷⣄⠀⢰⣶⣿⣾⣭⣿⣋⣭⣷⡿⢿⣿⡿⢷⣄⠀⠛⠻⢿⣂⠀⠀⠀⠀⠈⣿ </tspan>
<tspan x="15" y="314">⣿⣿⣿⣿⣦⢸⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠋⠁⠀⠩⣄⣾⣿⣿⣿⠀⠀⠀⠀⣀⣿ </tspan>
<tspan x="15" y="336">⣿⣿⣿⣿⠋⢸⣿⣿⣿⣿⣿⠿⣫⣿⣿⣿⣿⣯⣷⡲⡈⠈⢿⣿⡿⠀⠀⣴⣾⣿ </tspan>
<tspan x="15" y="358">⣿⣿⣿⣿⣾⠆⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⡉⠉⠹⣿⣶⡀⢸⣿⠁⠀⣈⣿⣿⣿ </tspan>
<tspan x="15" y="380">⣿⣿⣿⣿⡏⠀⠸⣿⣿⣿⣯⣿⣿⠛⠉⠿⠇⠀⠀⠈⠉⠁⠈⠋⠀⢀⣻⣿⣿⣿ </tspan>
<tspan x="15" y="402">⠿⠛⠉⠙⡗⠀⠀⠀⣝⠻⠛⠻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠿⢿⣿ </tspan>
<tspan x="15" y="424">⠀⠀⠀⠀⠃⠀⠀⠀⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿ </tspan>
<tspan x="15" y="446">⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣶⠄⠀⣰⣶⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿ </tspan>
<tspan x="15" y="468">⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⡿⠀⠈⠛⠳⠽⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻ </tspan>
<tspan x="15" y="490">⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀</tspan>
<tspan x="15" y="512">⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⠀⠀⠀</tspan>
<tspan x="15" y="534">⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢲⣀⠀⠀⠀</tspan>
<tspan x="15" y=""> </tspan>
</text>
<text x="390" y="30" fill="#c9d1d9">
<tspan x="390" y="30">MinhajShafin</tspan> -———————————————————————————————————————————-—-
<tspan x="390" y="50" class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">Android 15, Linux Mint 22.2</tspan>
<tspan x="390" y="70" class="cc">. </tspan><tspan class="key">Uptime</tspan>:<tspan class="cc" id="age_data_dots">{age_dots}</tspan><tspan class="value" id="age_data">{age_string}</tspan>
<tspan x="390" y="90" class="cc">. </tspan>
<tspan x="390" y="110" class="cc">. </tspan>
<tspan x="390" y="130" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan class="cc"> ...............................................</tspan><tspan class="value">VSCode</tspan>
<tspan x="390" y="150" class="cc">. </tspan>
<tspan x="390" y="170" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:<tspan class="cc"> ..... </tspan><tspan class="value">Java, Python, JavaScript, C++</tspan>
<tspan x="390" y="190" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Computer</tspan>:<tspan class="cc"> ...................... </tspan><tspan class="value">HTML, CSS, JSON</tspan>
<tspan x="390" y="210" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Real</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">Bangla, English, Deutch</tspan>
<tspan x="390" y="230" class="cc">. </tspan>
<tspan x="390" y="250" class="cc">. </tspan><tspan class="key">Hobbies</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">Cinephillia, Photography</tspan>
<tspan x="390" y="270" class="cc">. </tspan><tspan class="key">Fuel</tspan>:<tspan class="cc"> ............................ </tspan><tspan class="value">Coffee, Pasta, Tiramisu</tspan>
<tspan x="390" y="310">- Contact</tspan> -——————————————————————————————————————————————-—-
<tspan x="390" y="330" class="cc">. </tspan><tspan class="key">Email</tspan>.<tspan class="key">Personal</tspan>:<tspan class="cc"> ................... </tspan><tspan class="value">minhajshafin@gmail.com</tspan>
<tspan x="390" y="350" class="cc">. </tspan><tspan class="key">Facebook</tspan>:<tspan class="cc"> .................................. </tspan><tspan class="value">Minhaj Shafin</tspan>
<tspan x="390" y="370" class="cc">. </tspan><tspan class="key">Instagram</tspan><tspan class="cc"> ..................................... </tspan><tspan class="value">billy_x__x</tspan>
<tspan x="390" y="390" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan class="cc"> ................................... </tspan><tspan class="value">MinhajShafin</tspan>
<tspan x="390" y="410" class="cc">. </tspan><tspan class="key">Discord</tspan>:<tspan class="cc"> ....................................... </tspan><tspan class="value">billy_x_x</tspan>
<tspan x="390" y="450">- GitHub Stats</tspan> -—————————————————————————————————————————-—-
<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots">{repo_dots}</tspan><tspan class="value" id="repo_data">{stats['repos']}</tspan> {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">{stats['contributed']}</tspan>}} | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots">{star_dots}</tspan><tspan class="value" id="star_data">{stats['stars']}</tspan>
<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Commmits</tspan>:<tspan class="cc" id="commit_data_dots">{commit_dots}</tspan><tspan class="value" id="commit_data">{stats['commits']}</tspan> | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots">{follower_dots}</tspan><tspan class="value" id="follower_data">{stats['followers']}</tspan>
<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots">{loc_dots}</tspan><tspan class="value" id="loc_data">{stats['loc_total']}</tspan> ( <tspan class="addColor" id="loc_add">{stats['loc_add']}</tspan><tspan class="addColor">++</tspan>, <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">{stats['loc_del']}</tspan><tspan class="delColor">--</tspan> )
</text>
</svg>
'''

    return svg_content

if __name__ == "__main__":
    print("🔄 Generating card.svg...")
    print("📊 Fetching GitHub stats...")
    svg = generate_card_svg()
    with open("card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✅ card.svg generated successfully with dynamic age and GitHub stats!")

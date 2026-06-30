#!/usr/bin/env python3
"""
Movie Recommendation System
An interactive CLI tool to recommend Indian movies based on user preferences.
"""

import os
import json
import sys

# ANSI Escape Sequences for terminal styling
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_movies():
    """Loads movies from movies.json."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "movies.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{RED}{BOLD}Error: 'movies.json' not found at {json_path}.{RESET}")
        print(f"Please ensure the file exists in the same directory as this script.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{RED}{BOLD}Error: 'movies.json' is not a valid JSON file.{RESET}")
        sys.exit(1)

def get_unique_genres(movies):
    """Dynamically extracts all unique genres from the movie dataset."""
    genres = set()
    for m in movies:
        for g in m.get("genres", []):
            genres.add(g.strip())
    return sorted(list(genres))

def get_unique_languages(movies):
    """Dynamically extracts all unique languages from the movie dataset."""
    languages = set()
    for m in movies:
        if "language" in m:
            languages.add(m["language"].strip())
    return sorted(list(languages))

def print_banner():
    """Displays a stylized application banner."""
    print(f"{BLUE}{BOLD}==================================================={RESET}")
    print(f"{CYAN}{BOLD}          🎥  MOVIE RECOMMENDATION SYSTEM  🎥          {RESET}")
    print(f"{BLUE}{BOLD}==================================================={RESET}")
    print(f"{WHITE}Explore & find the best Indian movies across genres!{RESET}\n")

def print_movie_table(movies):
    """Displays a list of movies in a beautifully formatted text table."""
    if not movies:
        print(f"\n{RED}No movies found matching your criteria.{RESET}\n")
        return
    
    # Calculate dynamic column widths based on longest string
    title_w = max(max(len(m['title']) for m in movies), 15)
    lang_w = max(max(len(m['language']) for m in movies), 8)
    dir_w = max(max(len(m['director']) for m in movies), 12)
    genre_w = max(max(len(", ".join(m['genres'])) for m in movies), 15)
    
    # Format and separators
    header_fmt = f"| {{:<{title_w}}} | {{:<4}} | {{:<{lang_w}}} | {{:<4}} | {{:<{dir_w}}} | {{:<{genre_w}}} |"
    divider = "+" + "-"*(title_w+2) + "+" + "-"*6 + "+" + "-"*(lang_w+2) + "+" + "-"*6 + "+" + "-"*(dir_w+2) + "+" + "-"*(genre_w+2) + "+"
    
    print(f"\n{CYAN}{divider}")
    print(header_fmt.format("Title", "Year", "Language", "IMDb", "Director", "Genres"))
    print(divider + RESET)
    
    for m in movies:
        genre_str = ", ".join(m['genres'])
        # Highlight highly rated movies (8.5+) in green, others in white
        color = GREEN if m['rating'] >= 8.5 else WHITE
        print(f"{color}" + header_fmt.format(m['title'], m['year'], m['language'], m['rating'], m['director'], genre_str) + f"{RESET}")
    
    print(f"{CYAN}{divider}{RESET}\n")

def display_synopsis(movies):
    """Allows user to inspect a movie's synopsis details."""
    while True:
        choice = input(f"Would you like to read the synopsis of any movie listed? (Enter Title or press Enter to skip): ").strip()
        if not choice:
            break
        
        # Search for exact or partial case-insensitive match
        match = None
        for m in movies:
            if choice.lower() in m['title'].lower():
                match = m
                break
        
        if match:
            print(f"\n{YELLOW}{BOLD}🍿 {match['title']} ({match['year']}) - {match['language']}{RESET}")
            print(f"{BOLD}Director:{RESET} {match['director']}")
            print(f"{BOLD}IMDb Rating:{RESET} ⭐ {match['rating']}/10")
            print(f"{BOLD}Genres:{RESET} {', '.join(match['genres'])}")
            print(f"{BOLD}Synopsis:{RESET} {match['synopsis']}\n")
        else:
            print(f"{RED}Movie '{choice}' not found in the current results table. Please try again.{RESET}\n")

def recommend_by_genre(movies):
    """Filter and recommend movies based on genre choice."""
    genres = get_unique_genres(movies)
    
    print(f"{BOLD}Available Genres:{RESET}")
    # Print genres in a clean grid format (3 items per line)
    for i in range(0, len(genres), 3):
        row = genres[i:i+3]
        print("  " + "  |  ".join(f"{YELLOW}{g}{RESET}" for g in row))
    print()
    
    selected = input("Enter a preferred genre: ").strip()
    if not selected:
        print(f"{RED}Genre cannot be empty.{RESET}\n")
        return
        
    filtered = []
    for m in movies:
        # Case insensitive matching for elements in genres list
        if any(selected.lower() == g.lower() for g in m.get("genres", [])):
            filtered.append(m)
            
    if filtered:
        print(f"\n{GREEN}{BOLD}🎉 Recommendations for Genre: '{selected.capitalize()}' ({len(filtered)} found){RESET}")
        # Sort recommendations by rating descending
        filtered.sort(key=lambda x: x['rating'], reverse=True)
        print_movie_table(filtered)
        display_synopsis(filtered)
    else:
        # Offer suggestions on mismatch
        print(f"\n{RED}No movies found under genre '{selected}'.{RESET}")
        suggestions = [g for g in genres if selected.lower() in g.lower()]
        if suggestions:
            print(f"Did you mean: {', '.join(suggestions)}?\n")
        else:
            print(f"Please try one of the available genres listed above.\n")

def search_by_title(movies):
    """Search movies by title text search."""
    term = input("Enter movie title to search: ").strip()
    if not term:
        print(f"{RED}Search term cannot be empty.{RESET}\n")
        return
        
    filtered = [m for m in movies if term.lower() in m['title'].lower()]
    if filtered:
        print(f"\n{GREEN}{BOLD}🔎 Search Results for: '{term}' ({len(filtered)} found){RESET}")
        print_movie_table(filtered)
        display_synopsis(filtered)
    else:
        print(f"\n{RED}No movies found matching '{term}'. Please try again.{RESET}\n")

def filter_by_language(movies):
    """Filter movies by language choice."""
    languages = get_unique_languages(movies)
    print(f"{BOLD}Available Languages:{RESET}")
    print("  " + ", ".join(f"{YELLOW}{l}{RESET}" for l in languages) + "\n")
    
    selected = input("Enter language: ").strip()
    if not selected:
        print(f"{RED}Language cannot be empty.{RESET}\n")
        return
        
    filtered = [m for m in movies if selected.lower() == m.get("language", "").lower()]
    if filtered:
        print(f"\n{GREEN}{BOLD}🌍 Movies in language: '{selected.capitalize()}' ({len(filtered)} found){RESET}")
        filtered.sort(key=lambda x: x['rating'], reverse=True)
        print_movie_table(filtered)
        display_synopsis(filtered)
    else:
        print(f"\n{RED}No movies found in language '{selected}'.\n{RESET}")

def view_top_rated(movies):
    """View top rated movies sorted by IMDb rating."""
    limit_input = input("How many top movies would you like to see? (Press Enter for all): ").strip()
    
    try:
        limit = int(limit_input) if limit_input else len(movies)
    except ValueError:
        print(f"{RED}Invalid input. Showing all top movies.{RESET}")
        limit = len(movies)
        
    sorted_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)[:limit]
    print(f"\n{GREEN}{BOLD}⭐ Top {len(sorted_movies)} Rated Movies{RESET}")
    print_movie_table(sorted_movies)
    display_synopsis(sorted_movies)

def main():
    movies = load_movies()
    
    clear_screen()
    while True:
        print_banner()
        print(f"{BOLD}Main Menu:{RESET}")
        print(f"  1. 🎭 Recommend by Genre")
        print(f"  2. 🔎 Search by Title")
        print(f"  3. 🌍 Filter by Language")
        print(f"  4. ⭐ View Top Rated Movies")
        print(f"  5. ❌ Exit")
        print()
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            clear_screen()
            print_banner()
            recommend_by_genre(movies)
        elif choice == '2':
            clear_screen()
            print_banner()
            search_by_title(movies)
        elif choice == '3':
            clear_screen()
            print_banner()
            filter_by_language(movies)
        elif choice == '4':
            clear_screen()
            print_banner()
            view_top_rated(movies)
        elif choice == '5':
            print(f"\n{GREEN}{BOLD}Thank you for using Movie Recommendation System. Enjoy your movie time! 🍿🎬{RESET}\n")
            break
        else:
            print(f"\n{RED}Invalid choice. Please choose a number between 1 and 5.{RESET}\n")
            
        input("Press Enter to return to the Main Menu...")
        clear_screen()

if __name__ == "__main__":
    # Windows CMD needs this to enable ANSI escape support
    if os.name == 'nt':
        os.system('')
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{GREEN}Goodbye! 🍿{RESET}\n")
        sys.exit(0)

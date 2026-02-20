import requests
import json
import csv
from datetime import datetime
import time

class LeetCodeAPIScraper:
    """
    Scrape LeetCode data using GraphQL API
    """
    
    def __init__(self):
        self.url = "https://leetcode.com/graphql"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/",
            "Accept": "*/*"
        }
        self.session = requests.Session()
    
    def query(self, query_string, verbose=False):
        """Execute GraphQL query"""
        payload = {"query": query_string.strip()}
        
        try:
            response = self.session.post(self.url, json=payload, headers=self.headers, timeout=15)
            
            if verbose:
                print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if "errors" in result:
                    print(f"  GraphQL Error: {result['errors']}")
                return result
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
                print(f"  Response: {response.text[:200]}")
                return None
        except Exception as e:
            print(f"  ❌ Request failed: {e}")
            return None
    
    def scrape_trending_users(self, limit=10):
        """
        Scrape top ranked users from LeetCode
        """
        print(f"\n📥 Scraping top {limit} ranked users...")
        
        # Query top users by global ranking
        query = """ 
        query {
            globalRanking {
                rankingNodes {
                    ranking
                    user {
                        username
                        profile {
                            realName
                            reputation
                            ranking
                        }
                    }
                }
            }
        }
        """
        
        result = self.query(query, verbose=True)
        
        if result and "data" in result and "globalRanking" in result["data"]:
            ranking_data = result["data"]["globalRanking"]
            users = []
            
            for idx, node in enumerate(ranking_data.get("rankingNodes", [])[:limit], 1):
                user = node.get("user", {})
                users.append({
                    "rank": node.get("ranking", idx),
                    "username": user.get("username", "N/A"),
                    "name": user.get("profile", {}).get("realName", "N/A"),
                    "reputation": user.get("profile", {}).get("reputation", 0),
                    "ranking": user.get("profile", {}).get("ranking", "N/A")
                })
                print(f"  ✅ {idx}. {user.get('username')} - {user.get('profile', {}).get('realName', 'N/A')}")
            
            return users
        
        print(f"  Response: {result}")
        print("  ❌ No data found")
        return None
    
    def scrape_user_profile(self, username):
        """
        Scrape detailed user profile with advanced stats
        """
        print(f"\n📥 Scraping profile: {username}")
        
        query = f"""
        query {{
            matchedUser(username: "{username}") {{
                username
                profile {{
                    realName
                    reputation
                    ranking
                    userAvatar
                }}
                submitStats {{
                    acSubmissionNum {{
                        difficulty
                        count
                    }}
                    totalSubmissionNum {{
                        difficulty
                        count
                    }}
                }}
                problemsSolvedBeatsStats {{
                    difficulty
                    percentage
                }}
                badges {{
                    displayName
                }}
                languageProblemCount {{
                    languageName
                    problemsSolved
                }}
            }}
            userContestRanking(username: "{username}") {{
                rating
                globalRanking
                totalParticipants
                attendedContestsCount
            }}
        }}
        """
        
        result = self.query(query, verbose=False)
        
        if result and "data" in result and "matchedUser" in result["data"]:
            user = result["data"]["matchedUser"]
            contest = result["data"].get("userContestRanking", {})
            
            if not user:
                print(f"  ❌ User not found")
                return None
            
            profile_data = {
                "username": user.get("username"),
                "real_name": user.get("profile", {}).get("realName"),
                "reputation": user.get("profile", {}).get("reputation"),
                "ranking": user.get("profile", {}).get("ranking"),
                "solved_easy": 0,
                "solved_medium": 0,
                "solved_hard": 0,
                "total_easy": 0,
                "total_medium": 0,
                "total_hard": 0,
                "beats_easy": 0,
                "beats_medium": 0,
                "beats_hard": 0,
                "contest_rating": contest.get("rating") if contest else None,
                "global_ranking": contest.get("globalRanking") if contest else None,
                "total_participants": contest.get("totalParticipants") if contest else None,
                "attended_contests": contest.get("attendedContestsCount", 0) if contest else 0,
                "badges": "N/A",
                "languages": "N/A",
                "top_percentage": 0
            }
            
            # Parse submission stats
            for stat in user.get("submitStats", {}).get("acSubmissionNum", []):
                difficulty = stat.get("difficulty", "").lower()
                count = stat.get("count", 0)
                if difficulty == "easy":
                    profile_data["solved_easy"] = count
                elif difficulty == "medium":
                    profile_data["solved_medium"] = count
                elif difficulty == "hard":
                    profile_data["solved_hard"] = count
            
            # Parse total submissions
            for stat in user.get("submitStats", {}).get("totalSubmissionNum", []):
                difficulty = stat.get("difficulty", "").lower()
                count = stat.get("count", 0)
                if difficulty == "easy":
                    profile_data["total_easy"] = count
                elif difficulty == "medium":
                    profile_data["total_medium"] = count
                elif difficulty == "hard":
                    profile_data["total_hard"] = count
            
            # Parse beats stats (percentiles)
            for stat in user.get("problemsSolvedBeatsStats", []):
                difficulty = stat.get("difficulty", "").lower()
                percentage = stat.get("percentage", 0)
                if difficulty == "easy":
                    profile_data["beats_easy"] = percentage
                elif difficulty == "medium":
                    profile_data["beats_medium"] = percentage
                elif difficulty == "hard":
                    profile_data["beats_hard"] = percentage
                    profile_data["top_percentage"] = percentage  # Use hard difficulty as overall top%
            
            # Parse badges
            badges = []
            for badge in user.get("badges", []):
                badges.append({
                    "name": badge.get("displayName"),
                    "icon": badge.get("medal", {}).get("config", {}).get("icon", "N/A")
                })
            profile_data["badges"] = badges
            
            # Parse languages
            languages = {}
            for lang in user.get("languageProblemCount", []):
                languages[lang.get("languageName")] = lang.get("problemsSolved", 0)
            profile_data["languages"] = languages
            
            # Parse skills by difficulty level
            for skill in user.get("skillTags", []):
                skill_name = skill.get("tagName")
                problems_solved = skill.get("problemsSolved", 0)
                
                if problems_solved > 10:
                    profile_data["skills_advanced"].append({
                        "name": skill_name,
                        "problems_solved": problems_solved
                    })
                elif problems_solved > 5:
                    profile_data["skills_intermediate"].append({
                        "name": skill_name,
                        "problems_solved": problems_solved
                    })
                else:
                    profile_data["skills_fundamental"].append({
                        "name": skill_name,
                        "problems_solved": problems_solved
                    })
            
            print(f"  ✅ Profile data scraped with advanced stats")
            return profile_data
        
        print(f"  ❌ Could not scrape profile")
        return None
    
    def scrape_user_contests(self, username):
        """
        Scrape user's contest information
        """
        print(f"  📥 Scraping contests: {username}")
        
        query = f"""
        query {{
            userContestRanking(username: "{username}") {{
                attendedContestsCount
                rating
                globalRanking
                totalParticipants
            }}
        }}
        """
        
        result = self.query(query, verbose=False)
        
        if result and "data" in result and "userContestRanking" in result["data"]:
            return result["data"]["userContestRanking"]
        
        return None
    
    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"  ✅ Saved to {filename}")
        except Exception as e:
            print(f"  ❌ Error saving JSON: {e}")
    
    def save_to_csv(self, data, filename, keys=None):
        """Save data to CSV file"""
        try:
            if not data:
                return
            
            if keys is None:
                keys = data[0].keys()
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            print(f"  ✅ Saved to {filename}")
        except Exception as e:
            print(f"  ❌ Error saving CSV: {e}")
    
    def display_table(self, data):
        """Display data in table format"""
        if not data:
            print("No data to display")
            return
        
        print("\n" + "="*180)
        
        # Select only key columns for display (exclude badges and languages)
        all_keys = list(data[0].keys())
        display_keys = [k for k in all_keys if k not in ['badges', 'languages', 'skills_advanced', 'skills_intermediate', 'skills_fundamental']]
        
        # Calculate column widths
        col_widths = {}
        for key in display_keys:
            max_len = len(str(key))
            for row in data:
                val = row.get(key, "")
                if isinstance(val, list):
                    val_str = f"{len(val)} items"
                elif isinstance(val, dict):
                    val_str = f"{len(val)} items" if val else "empty"
                else:
                    val_str = str(val) if val is not None else "N/A"
                max_len = max(max_len, len(val_str))
            col_widths[key] = min(max_len, 25)  # Cap at 25 chars
        
        # Print header
        header = " | ".join(f"{key:<{col_widths[key]}}" for key in display_keys)
        print(header)
        print("-" * min(len(header), 180))
        
        # Print rows
        for row in data:
            row_values = []
            for key in display_keys:
                val = row.get(key, "")
                if isinstance(val, list):
                    val_str = f"{len(val)} items"
                elif isinstance(val, dict):
                    val_str = f"{len(val)} items" if val else "empty"
                else:
                    val_str = str(val) if val is not None else "N/A"
                
                # Truncate if too long
                if len(val_str) > 25:
                    val_str = val_str[:22] + "..."
                row_values.append(f"{val_str:<{col_widths[key]}}")
            
            row_str = " | ".join(row_values)
            print(row_str)
        
        
        print("="*120)


def main():
    print("\n" + "="*120)
    print("🚀 LeetCode API Scraper")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*120)
    
    scraper = LeetCodeAPIScraper()
    
    # 1. Scrape trending users
    trending_users = scraper.scrape_trending_users(limit=10)
    
    if not trending_users:
        print("❌ Failed to scrape trending users")
        return
    
    # Display trending users
    scraper.display_table(trending_users)
    
    # Save trending users
    scraper.save_to_json(trending_users, "trending_users.json")
    scraper.save_to_csv(trending_users, "trending_users.csv")
    
    # 2. Scrape detailed profiles for each user
    print(f"\n{'='*120}")
    print("📦 Scraping detailed profiles...")
    print("="*120)
    
    all_profiles = []
    usernames = [u["username"] for u in trending_users]
    
    for username in usernames:
        profile = scraper.scrape_user_profile(username)
        
        if profile:
            all_profiles.append(profile)
            print(f"    Solved: Easy={profile['solved_easy']}, Medium={profile['solved_medium']}, Hard={profile['solved_hard']}")
        
        time.sleep(1)  # Be respectful with API
    
    # Display profiles
    if all_profiles:
        print(f"\n{'='*120}")
        print("User Profiles")
        print("="*120)
        scraper.display_table(all_profiles)
        
        # Save profiles
        scraper.save_to_json(all_profiles, "user_profiles.json")
        scraper.save_to_csv(all_profiles, "user_profiles.csv")
    
    # 3. Scrape contests
    print(f"\n{'='*120}")
    print("📦 Scraping contest information...")
    print("="*120)
    
    all_contests = []
    for username in usernames[:5]:  # Limit to first 5 to avoid too many requests
        print(f"Scraping {username}...")
        contests = scraper.scrape_user_contests(username)
        
        if contests:
            contests["username"] = username
            all_contests.append(contests)
            print(f"  Rating: {contests.get('rating')}, Global Rank: {contests.get('globalRanking')}")
        
        time.sleep(1)
    
    if all_contests:
        scraper.display_table(all_contests)
        scraper.save_to_json(all_contests, "user_contests.json")
        scraper.save_to_csv(all_contests, "user_contests.csv")
    
    # Summary
    print(f"\n{'='*120}")
    print("✅ Scraping Complete!")
    print("="*120)
    print(f"📁 Files saved:")
    print(f"  - trending_users.json")
    print(f"  - trending_users.csv")
    print(f"  - user_profiles.json")
    print(f"  - user_profiles.csv")
    if all_contests:
        print(f"  - user_contests.json")
        print(f"  - user_contests.csv")
    print(f"\n📊 Total users scraped: {len(trending_users)}")
    print(f"📊 Total profiles: {len(all_profiles)}")
    print(f"📊 Contest records: {len(all_contests)}")
    print("="*120 + "\n")


if __name__ == "__main__":
    main()

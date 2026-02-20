import requests
import time
import json
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURATION ---
LEETCODE_URL = "https://leetcode.com/graphql"
TOTAL_RECORDS_WANTED = 10000
PAGE_SIZE = 25  # LeetCode usually returns 25 users per ranking page
BATCH_SAVE_INTERVAL = 100  # Save to CSV every 100 profiles

# Headers are critical to avoid 403 Forbidden from Cloudflare
# You might need to update the 'Cookie' if you face strict blocking, 
# but usually, a good User-Agent is enough for public data.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com/",
}

# --- GRAPHQL QUERIES ---

# 1. Query to get a list of usernames from the global ranking
QUERY_GLOBAL_RANKING = """
query globalRanking($page: Int) {
  globalRanking(page: $page) {
    rankingNodes {
      currentRating
      currentGlobalRanking
      dataRegion
      user {
        username
        profile {
          countryName
          realName
        }
      }
    }
  }
}
"""

# 2. Query to get detailed profile features for a specific user
QUERY_USER_PROFILE = """
query userPublicProfile($username: String!) {
  matchedUser(username: $username) {
    username
    githubUrl
    twitterUrl
    linkedinUrl
    profile {
      ranking
      userAvatar
      realName
      aboutMe
      school
      websites
      countryName
      company
      jobTitle
      skillTags
      postViewCount
      reputation
      solutionCount
    }
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
    badges {
      id
      displayName
      icon
    }
    upcomingBadges {
      name
      icon
    }
    activeBadge {
      displayName
      id
    }
  }
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    topPercentage
    badge {
      name
    }
  }
}
"""

def fetch_graphql(query, variables):
    """Generic function to execute a GraphQL query."""
    payload = {
        "query": query,
        "variables": variables
    }
    
    for attempt in range(3):
        try:
            response = requests.post(LEETCODE_URL, headers=HEADERS, json=payload, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"⚠️ Rate limited. Sleeping for {10 * (attempt + 1)} seconds...")
                time.sleep(10 * (attempt + 1))
            else:
                print(f"❌ Error {response.status_code}: {response.text[:100]}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            time.sleep(5)
            
    return None

def get_usernames(limit=1000):
    """Fetches usernames from the global ranking pages."""
    usernames = []
    total_pages = (limit // PAGE_SIZE) + 1
    
    print(f"🔍 Fetching {limit} usernames from Global Ranking...")
    
    for page in range(1, total_pages + 1):
        data = fetch_graphql(QUERY_GLOBAL_RANKING, {"page": page})
        
        if not data or "data" not in data:
            continue
            
        nodes = data["data"]["globalRanking"]["rankingNodes"]
        for node in nodes:
            # We only want valid users
            if node["user"]:
                usernames.append(node["user"]["username"])
        
        print(f"   Page {page}/{total_pages} done. Total users found: {len(usernames)}")
        
        # Rate limit protection: Sleep between requests
        time.sleep(random.uniform(1.0, 3.0)) 
        
        if len(usernames) >= limit:
            break
            
    return usernames[:limit]

def process_user_data(username, full_data):
    """Parses the nested GraphQL JSON into a flat dictionary."""
    if not full_data or "data" not in full_data or not full_data["data"]["matchedUser"]:
        return None
    
    user_data = full_data["data"]["matchedUser"]
    contest_data = full_data["data"].get("userContestRanking") or {}
    profile = user_data.get("profile") or {}
    submit_stats = user_data.get("submitStats", {}).get("acSubmissionNum", [])
    
    # Flatten submission stats (Easy/Medium/Hard)
    solved_all = next((item["count"] for item in submit_stats if item["difficulty"] == "All"), 0)
    solved_easy = next((item["count"] for item in submit_stats if item["difficulty"] == "Easy"), 0)
    solved_medium = next((item["count"] for item in submit_stats if item["difficulty"] == "Medium"), 0)
    solved_hard = next((item["count"] for item in submit_stats if item["difficulty"] == "Hard"), 0)

    # Extract Badges
    badges = [b["displayName"] for b in user_data.get("badges", [])]
    
    record = {
        "username": user_data.get("username"),
        "real_name": profile.get("realName"),
        "country": profile.get("countryName"),
        "school": profile.get("school"),
        "company": profile.get("company"),
        "ranking": profile.get("ranking"),
        "reputation": profile.get("reputation"),
        "solved_total": solved_all,
        "solved_easy": solved_easy,
        "solved_medium": solved_medium,
        "solved_hard": solved_hard,
        "contest_rating": int(contest_data.get("rating")) if contest_data and contest_data.get("rating") else None,
        "contest_global_rank": contest_data.get("globalRanking"),
        "attended_contests": contest_data.get("attendedContestsCount"),
        "skills": ", ".join(profile.get("skillTags", [])),
        "badges_count": len(badges),
        "badges": ", ".join(badges),
        "github_url": user_data.get("githubUrl"),
        "linkedin_url": user_data.get("linkedinUrl"),
        "twitter_url": user_data.get("twitterUrl"),
    }
    return record

def main():
    # 1. Get Usernames
    usernames = get_usernames(limit=TOTAL_RECORDS_WANTED)
    print(f"✅ Collected {len(usernames)} usernames. Starting detailed profile fetch...")
    
    all_records = []
    
    # 2. Fetch Details for each user
    for i, username in enumerate(usernames):
        print(f"[{i+1}/{len(usernames)}] Fetching: {username}")
        
        raw_data = fetch_graphql(QUERY_USER_PROFILE, {"username": username})
        record = process_user_data(username, raw_data)
        
        if record:
            all_records.append(record)
        
        # Save periodically in case script crashes
        if (i + 1) % BATCH_SAVE_INTERVAL == 0:
            df = pd.DataFrame(all_records)
            df.to_csv("leetcode_users_partial_1.csv", index=False)
            print(f"💾 Saved {len(all_records)} records to CSV.")
        
        # IMPORTANT: Rate limiting sleep
        # If you go too fast, LeetCode will start returning nulls or 429s.
        time.sleep(random.uniform(0.5, 1.5))

    # Final Save
    df = pd.DataFrame(all_records)
    df.to_csv("leetcode_users_final.csv", index=False)
    print("🎉 Done! Data saved to leetcode_users_final.csv")

if __name__ == "__main__":
    main()
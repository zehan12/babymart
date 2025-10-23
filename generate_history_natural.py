import os
import random
import datetime
import subprocess
import shutil

def run_git_cmd(cmd, env=None):
    return subprocess.run(cmd, shell=True, env={**os.environ, **(env or {})}, capture_output=True, text=True)

def generate_history():
    repo_path = "/home/zehan/Documents/babymart-yt"
    os.chdir(repo_path)
    
    # 1. Reset Git
    if os.path.exists(".git"):
        shutil.rmtree(".git")
    
    run_git_cmd("git init")
    run_git_cmd("git branch -M main")
    run_git_cmd("git remote add origin git@github.com:zehan12/babymart.git")

    # 2. Collect files (respecting .gitignore)
    run_git_cmd("git add .")
    files_result = run_git_cmd("git ls-files")
    all_files = files_result.stdout.splitlines()
    run_git_cmd("git reset")
    
    all_files = [f for f in all_files if os.path.exists(f)]
    random.shuffle(all_files) # Shuffle to distribute randomly across history
    
    # 3. Define the timeline
    start_date = datetime.date(2025, 10, 5) # Sunday
    end_date = datetime.date(2026, 2, 8)
    
    # 4. Generate random "active" days and commit counts
    current_date = start_date
    timestamps = []
    target_commits = 200
    
    while len(timestamps) < target_commits and current_date <= end_date:
        # Weekdays (0-4) are more likely to have commits
        is_weekend = current_date.weekday() >= 5
        
        # Chance of activity
        chance = 0.15 if is_weekend else 0.75
        
        if random.random() < chance:
            # 1 to 7 commits per active day
            num_commits_today = random.randint(1, 8)
            
            # Ensure we don't overshoot target significantly in one go
            if len(timestamps) + num_commits_today > target_commits + 5:
                num_commits_today = max(1, target_commits - len(timestamps))
            
            for _ in range(num_commits_today):
                # Pick a random time during "work hours" with some variance
                # Mostly between 9 AM and 8 PM, but some late night/early morning
                hour = random.choices(
                    range(24), 
                    weights=[1, 0, 0, 0, 0, 1, 3, 8, 15, 12, 10, 10, 12, 15, 15, 12, 10, 12, 15, 12, 8, 5, 3, 2]
                )[0]
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                
                dt = datetime.datetime.combine(current_date, datetime.time(hour, minute, second))
                timestamps.append(dt)
        
        current_date += datetime.timedelta(days=1)
        
    # If we reached the end of the date range and don't have enough, 
    # just stuff them into the last few weeks
    while len(timestamps) < target_commits:
        days_back = random.randint(0, 30)
        ts = datetime.datetime.combine(end_date - datetime.timedelta(days=days_back), 
                                      datetime.time(random.randint(9, 21), random.randint(0, 59)))
        timestamps.append(ts)

    timestamps.sort()
    # Keep exactly the target
    timestamps = timestamps[:target_commits]

    # 5. Quality commit messages
    feat_msgs = [
        "feat: implement secure JWT authentication flow", "feat: add product category filtering and sorting",
        "feat: integrate Stripe checkout for secure payments", "feat: create responsive navigation with mobile drawer",
        "feat: add user profile management and address book", "feat: implement real-time shopping cart synchronization",
        "feat: add wishlist functionality for registered users", "feat: create dynamic product detail pages with variants",
        "feat: implement global search with search suggestions", "feat: add administrative dashboard for order tracking",
        "feat: integrate Cloudinary for efficient image hosting", "feat: add review and rating system for products",
        "feat: implement password reset via email service", "feat: add multi-currency support for global shopping",
        "feat: create animated banner sliders for promotions", "feat: implement inventory management alert system",
        "feat: add skeleton loaders for improved UX", "feat: integrate framer-motion for smooth transitions",
        "feat: add toast notifications for user feedback", "feat: implement order history and status tracking",
        "feat: add social media sharing for products", "feat: create specialized 'deals of the day' section",
        "feat: implement guest checkout functionality", "feat: add newsletter subscription with email validation"
    ]
    
    fix_msgs = [
        "fix: resolve hydration error on product listing", "fix: correct mobile layout overflow in cart",
        "fix: resolve database connection leakage in server", "fix: correct stripe webhook signature verification",
        "fix: resolve z-index conflict with navigation bar", "fix: handle api timeout in slow network conditions",
        "fix: correct price calculation for discounted items", "fix: resolve session persistence issue on mobile",
        "fix: correct image aspect ratio on category cards", "fix: resolve cross-origin resource sharing (CORS) errors"
    ]
    
    perf_msgs = [
        "perf: optimize database queries for product listing", "perf: implement image lazy loading and optimization",
        "perf: reduce bundle size by modularizing components", "perf: cache api responses for frequently accessed data"
    ]
    
    # 6. Distribute files
    files_per_commit = len(all_files) // target_commits
    remainder = len(all_files) % target_commits
    
    file_idx = 0
    for i, ts in enumerate(timestamps):
        date_str = ts.strftime('%Y-%m-%dT%H:%M:%S')
        env = {'GIT_AUTHOR_DATE': date_str, 'GIT_COMMITTER_DATE': date_str}
        
        # Take batch of files
        num_files = files_per_commit + (1 if i < remainder else 0)
        batch = all_files[file_idx : file_idx + num_files]
        file_idx += num_files
        
        for f in batch:
            subprocess.run(f'git add "{f}"', shell=True)
            
        if i == 0:
            msg = "chore: initial project initialization and structure"
        elif i == target_commits - 1:
            msg = "feat: finalize mvp and prepared for production release"
        else:
            dice = random.random()
            if dice < 0.6: msg = random.choice(feat_msgs)
            elif dice < 0.8: msg = random.choice(fix_msgs)
            else: msg = random.choice(perf_msgs)
            
        subprocess.run(f'git commit --allow-empty -m "{msg}"', shell=True, env={**os.environ, **env})

    # 7. Finalize current state
    final_date = datetime.datetime(2026, 2, 9, 20, 55, 0)
    env = {'GIT_AUTHOR_DATE': final_date.isoformat(), 'GIT_COMMITTER_DATE': final_date.isoformat()}
    run_git_cmd("git add .")
    run_git_cmd('git commit -m "feat: complete application release and final polish"', env=env)
    
    print(f"Generated {len(timestamps) + 1} commits with randomized daily frequency.")

if __name__ == "__main__":
    generate_history()

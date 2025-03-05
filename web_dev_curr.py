from fpdf import FPDF

# Create PDF document
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "Intensive Web Development Curriculum", ln=True, align="C")

# Program Overview
pdf.ln(10)
pdf.set_font("Arial", size=12)
program_overview = """
Program Overview
Duration: 6 months
Focus: Full-stack web development with a real-world work environment
Technologies: HTML, CSS, JavaScript, React & Redux, Ruby, Ruby on Rails, SQL (PostgreSQL/MySQL), Python, Django, Vue.js, Java, Spring Boot
Methodology:
- Daily Activities: Solo learning, group tasks, coding challenges, and self-learning
- Capstone Projects: Weekly and monthly hands-on projects
- Soft Skills: Integrated lessons on communication, teamwork, and problem-solving
- Work Environment Simulation:
    Standup Meetings: Every morning (progress updates, blockers)
    Evening Retrospectives: Daily review and feedback sessions
"""
pdf.multi_cell(0, 10, program_overview)

# Phase 1: Foundations
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, "Phase 1: Foundations (Weeks 1-4)", ln=True)

# Week 1
week_1 = """
Week 1: Introduction to HTML & CSS
Lessons: HTML Structure, CSS Styling, Flexbox, Grid, Accessibility
Activities:
- Solo: Build a personal landing page
- Group: CSS layout challenges
- Task: Code a responsive webpage
- Self-Learning: Best practices in UI/UX
Capstone: Build a responsive portfolio site
Soft Skills Focus: Effective communication in remote teams
"""
pdf.multi_cell(0, 10, week_1)

# Week 2
week_2 = """
Week 2: JavaScript Fundamentals
Lessons: Data Types, Functions, Loops, DOM Manipulation
Activities:
- Solo: Solve JavaScript coding challenges
- Group: DOM event-driven project
- Task: Build a dynamic to-do list app
Capstone: Interactive website project
Soft Skills Focus: Problem-solving & debugging techniques
"""
pdf.multi_cell(0, 10, week_2)

# Week 3
week_3 = """
Week 3: Advanced JavaScript & Introduction to React
Lessons: ES6+, Fetch API, React Basics (Components, Props, State)
Activities:
- Solo: Build a React-based weather app
- Group: Collaborate on a React project
- Task: API integration practice
Capstone: Develop a React-based dashboard
Soft Skills Focus: Time management & goal setting
"""
pdf.multi_cell(0, 10, week_3)

# Week 4
week_4 = """
Week 4: Git, Agile, and Team Collaboration
Lessons: Version control, Git workflows, Agile methodologies
Activities:
- Solo: Git branching exercises
- Group: Work on an open-source project
- Task: Implement a feature in a team project
Capstone: Team-based project using Agile methodology
Soft Skills Focus: Collaboration & leadership
"""
pdf.multi_cell(0, 10, week_4)

# Phase 2: Backend Development & Databases
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, "Phase 2: Backend Development & Databases (Weeks 5-8)", ln=True)

# Week 5
week_5 = """
Week 5: Introduction to Ruby, Python, Java Syntax & OOP Principles
Lessons: Ruby, Python, Java syntax, Control Structures, OOP Principles
Activities:
- Solo: Ruby, Python, Java coding challenges
- Group: Build a command-line Ruby project
- Task: Implement OOP concepts in a small app
Capstone: CLI-based application
Soft Skills Focus: Giving and receiving feedback
"""
pdf.multi_cell(0, 10, week_5)

# Week 6
week_6 = """
Week 6: Databases & SQL
Lessons: PostgreSQL/MySQL Basics, Queries, Relationships
Activities:
- Solo: Write SQL queries to manage data
- Group: Design a database schema
- Task: Integrate a database into a simple app
Capstone: CRUD web application
Soft Skills Focus: Critical thinking & data analysis
"""
pdf.multi_cell(0, 10, week_6)

# Week 7
week_7 = """
Week 7: Ruby on Rails, Django, Laravel, Spring Boot Basics
Lessons: MVC Architecture, Routing, Active Record
Activities:
- Solo: Build a simple Rails app
- Group: Pair program a Rails feature
- Task: Implement RESTful APIs in Rails
Capstone: Mini web application
Soft Skills Focus: Technical writing & documentation
"""
pdf.multi_cell(0, 10, week_7)

# Week 8
week_8 = """
Week 8: Advanced Ruby on Rails or Django or Spring Boot, Laravel & APIs
Lessons: Authentication, Authorization, API Development
Activities:
- Solo: Secure a Rails, Django, Spring Boot, Laravel app with authentication
- Group: Build a Rails API for a frontend app
- Task: Integrate an external API
Capstone: Full authentication system
Soft Skills Focus: Conflict resolution & teamwork
"""
pdf.multi_cell(0, 10, week_8)

# Phase 3: Full-Stack Development
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, "Phase 3: Full-Stack Development (Weeks 9-12)", ln=True)

# Week 9
week_9 = """
Week 9: Frontend & Backend Integration
Lessons: Connecting React or Vue.js with Rails API
Activities:
- Solo: Fetch and display API data in React or Vue.js
- Group: Work on a full-stack app
- Task: Debug API and frontend issues
Capstone: Full-stack CRUD application
Soft Skills Focus: Managing work under deadlines
"""
pdf.multi_cell(0, 10, week_9)

# Week 10
week_10 = """
Week 10: Advanced React, Vue.js, Angular, Redux, Pinia
Lessons: State Management, Middleware, Optimizations
Activities:
- Solo: Implement Redux in a React app or Pinia in a Vue.js app
- Group: Refactor a React/Vue app with state management
- Task: Improve performance in a React or Vue.js project
Capstone: Scalable React/Vue application
Soft Skills Focus: Leadership in development teams
"""
pdf.multi_cell(0, 10, week_10)

# Week 11
week_11 = """
Week 11: Testing & Debugging
Lessons: Unit Testing, Integration Testing, Debugging Techniques
Activities:
- Solo: Write unit tests for a JavaScript or Python project
- Group: Debug and optimize a project
- Task: Test API endpoints
Capstone: Fully tested full-stack project
Soft Skills Focus: Adaptability & resilience
"""
pdf.multi_cell(0, 10, week_11)

# Week 12
week_12 = """
Week 12: DevOps & Deployment
Lessons: Docker, CI/CD, Cloud Deployment (AWS/GCP)
Activities:
- Solo: Deploy a Rails or Django app
- Group: Automate deployment with CI/CD
- Task: Set up a monitoring system
Capstone: Deploy a full-stack app to production
Soft Skills Focus: Handling real-world production issues
"""
pdf.multi_cell(0, 10, week_12)

# Final Capstone & Career Preparation
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, "Final Capstone & Career Preparation (Weeks 13-16)", ln=True)

final_capstone = """
- Build a Full-Scale Project (Choose an industry focus: E-commerce, Social Media, FinTech, etc.)
- Code Reviews & Feedback Sessions
- Mock Technical Interviews & Whiteboarding
- Resume & LinkedIn Profile Optimization
- Networking & Open-Source Contributions
"""
pdf.multi_cell(0, 10, final_capstone)

# Final Thoughts
final_thoughts = """
This curriculum now integrates Python, Django, Java, Spring Boot, and Vue.js alongside other key technologies. 
It remains focused on real-world skills and collaboration, with practical capstone projects that simulate a high-demand software engineering work environment.
"""
pdf.multi_cell(0, 10, final_thoughts)

# Save PDF
pdf_output_path = "/mnt/data/intensive_web_development_curriculum.pdf"
pdf.output(pdf_output_path)

pdf_output_path

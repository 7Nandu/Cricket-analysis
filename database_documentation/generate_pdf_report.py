import os
import sys
from fpdf import FPDF
from PIL import Image

class CricketReportPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=False, margin=14)
        self.set_margins(15, 14, 15)
        
        # Load Times New Roman TrueType fonts for native UTF-8 and bullet support
        self.add_font('TimesNR', '', r'C:\Windows\Fonts\times.ttf')
        self.add_font('TimesNR', 'B', r'C:\Windows\Fonts\timesbd.ttf')
        self.add_font('TimesNR', 'I', r'C:\Windows\Fonts\timesi.ttf')
        self.add_font('TimesNR', 'BI', r'C:\Windows\Fonts\timesbi.ttf')
        self.alias_nb_pages()

    def header(self):
        if self.page_no() == 1:
            return  # Suppress on title page
        
        self.set_font('TimesNR', 'I', 8.5)
        self.set_text_color(0, 0, 0)
        self.cell(110, 5.5, 'Cricket Analytics Database Project Report | CS-302 DBMS Laboratory', border=0, align='L')
        self.set_font('TimesNR', '', 8.5)
        self.cell(70, 5.5, 'B.Tech Computer Science & Engineering', border=0, align='R', new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.line(15, 19.5, 195, 19.5)
        self.ln(2)

    def footer(self):
        if self.page_no() == 1:
            return  # Suppress on title page

        self.set_y(-12)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.set_y(-10.5)
        self.set_font('TimesNR', '', 8.5)
        self.set_text_color(0, 0, 0)
        self.cell(100, 5.5, 'Academic Session 2025-2026 | PostgreSQL Relational Database System', border=0, align='L')
        self.cell(80, 5.5, f'Page {self.page_no()} of {{nb}}', border=0, align='R')

    def chapter_heading(self, number, title):
        self.set_font('TimesNR', 'B', 11.5)
        self.set_text_color(0, 0, 0)
        heading_text = f"{number}. {title}" if number else title
        self.cell(0, 6, heading_text, border='B', new_x="LMARGIN", new_y="NEXT")
        self.ln(1.5)

    def section_heading(self, title):
        self.set_font('TimesNR', 'B', 9.8)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.8)

    def bullet(self, title, text, indent=0, ln=True):
        self.set_font('TimesNR', '', 9.0)
        self.set_text_color(0, 0, 0)
        prefix = "    " * indent
        bold_title = f"**• {title}:** " if title else "**•** "
        md_text = f"{prefix}{bold_title}{text}"
        self.multi_cell(0, 4.1, md_text, markdown=True, align='J')
        if ln:
            self.ln(1.2)

    def sub_bullet(self, title, text, ln=True):
        self.set_font('TimesNR', '', 8.8)
        self.set_text_color(0, 0, 0)
        bold_title = f"**– {title}:** " if title else "**–** "
        md_text = f"    {bold_title}{text}"
        self.multi_cell(0, 3.9, md_text, markdown=True, align='J')
        if ln:
            self.ln(1.0)

    def render_table(self, headers, data, widths):
        self.set_font('TimesNR', 'B', 8.2)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        
        for i, header in enumerate(headers):
            col_align = 'C' if i in [0, 2, 3] and len(header) < 15 else 'L'
            self.cell(widths[i], 5.2, header, border=1, align=col_align, fill=True)
        self.ln()

        self.set_font('TimesNR', '', 8.0)
        self.set_text_color(0, 0, 0)
        
        for r_idx, row in enumerate(data):
            for c_idx, cell_value in enumerate(row):
                col_align = 'C' if c_idx in [0, 2, 3] and len(str(cell_value)) < 15 else 'L'
                self.cell(widths[c_idx], 4.5, str(cell_value), border=1, align=col_align, fill=False)
            self.ln()
        self.ln(1.8)

    def code_box(self, sql_text, caption=""):
        if caption:
            self.set_font('TimesNR', 'B', 8.2)
            self.set_text_color(0, 0, 0)
            self.cell(0, 4.0, f"Listing: {caption}", new_x="LMARGIN", new_y="NEXT")
        
        self.set_fill_color(248, 248, 248)
        self.set_draw_color(0, 0, 0)
        self.set_font('Courier', '', 7.3)
        self.set_text_color(0, 0, 0)
        
        lines = sql_text.strip().split('\n')
        box_height = len(lines) * 3.8 + 3
        x = self.get_x()
        y = self.get_y()
        self.rect(x, y, 180, box_height, 'DF')
        
        self.set_xy(x + 2, y + 1.5)
        for line in lines:
            self.cell(176, 3.8, line, new_x="LMARGIN", new_y="NEXT")
        self.set_y(y + box_height + 1.8)


def generate_report():
    pdf = CricketReportPDF()

    # =========================================================================
    # PAGE 1: TITLE PAGE (BULLET STRUCTURED METADATA, MONOCHROME, TIMES NEW ROMAN)
    # =========================================================================
    pdf.add_page()
    
    # Outer Border
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(1.0)
    pdf.rect(12, 12, 186, 273)
    pdf.set_line_width(0.3)
    pdf.rect(13.5, 13.5, 183, 270)

    pdf.set_y(26)
    pdf.set_font('TimesNR', 'B', 13)
    pdf.cell(0, 6, "A TECHNICAL SEMESTER PROJECT REPORT", align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(1.5)
    pdf.set_font('TimesNR', '', 10)
    pdf.cell(0, 5, "COURSE: CS-302 | DATABASE MANAGEMENT SYSTEMS LABORATORY", align='C', new_x="LMARGIN", new_y="NEXT")

    pdf.ln(16)
    # Title Box
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.8)
    pdf.rect(20, 56, 170, 50)

    pdf.set_y(62)
    pdf.set_font('TimesNR', 'B', 18)
    pdf.cell(0, 8.5, "CRICKET ANALYTICS SYSTEM", align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(1.5)
    pdf.set_font('TimesNR', 'B', 11)
    pdf.cell(0, 5.5, "A 3NF Relational Database Architecture and Interactive Web Dashboard", align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('TimesNR', 'I', 9.5)
    pdf.cell(0, 5, "Complete Database Documentation, Cardinality Analysis, Constraints & Procedural Triggers", align='C', new_x="LMARGIN", new_y="NEXT")

    pdf.ln(34)
    # Divider Rule
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(75, 122, 135, 122)

    pdf.set_y(130)
    pdf.set_font('TimesNR', 'B', 10)
    pdf.cell(0, 5.5, "SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE DEGREE OF", align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('TimesNR', 'B', 12.5)
    pdf.cell(0, 6.5, "BACHELOR OF TECHNOLOGY", align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('TimesNR', '', 10)
    pdf.cell(0, 5, "IN COMPUTER SCIENCE AND ENGINEERING", align='C', new_x="LMARGIN", new_y="NEXT")

    pdf.ln(24)
    # Metadata Cards (Structured as clean bullet lists)
    y_meta = 176
    
    # Left Card: Student Credentials
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    pdf.rect(25, y_meta, 75, 56)
    pdf.set_y(y_meta + 4)
    pdf.set_x(28)
    pdf.set_font('TimesNR', 'B', 9.5)
    pdf.cell(70, 4.5, "CANDIDATE INFORMATION:", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    
    pdf.set_x(28)
    pdf.set_font('TimesNR', '', 9.0)
    pdf.cell(70, 4.2, "• Name: Ashmita Bhattacharya", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(28)
    pdf.cell(70, 4.2, "• University Roll No: 2023-CS-114", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(28)
    pdf.cell(70, 4.2, "• Academic Semester: V (3rd Year)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(28)
    pdf.cell(70, 4.2, "• Program: B.Tech Computer Science", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(28)
    pdf.cell(70, 4.2, "• Track: Data & Database Systems", new_x="LMARGIN", new_y="NEXT")

    # Right Card: Academic Guidance & Institution
    pdf.rect(110, y_meta, 75, 56)
    pdf.set_y(y_meta + 4)
    pdf.set_x(113)
    pdf.set_font('TimesNR', 'B', 9.5)
    pdf.cell(70, 4.5, "INSTITUTIONAL SUPERVISION:", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    
    pdf.set_x(113)
    pdf.set_font('TimesNR', '', 9.0)
    pdf.cell(70, 4.2, "• Dept: Computer Science & Engg.", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(113)
    pdf.cell(70, 4.2, "• Faculty: Engineering & Technology", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(113)
    pdf.cell(70, 4.2, "• Lab: Database Systems & Analytics", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(113)
    pdf.cell(70, 4.2, "• Target Engine: PostgreSQL 16.x", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(113)
    pdf.cell(70, 4.2, "• Academic Session: 2025 - 2026", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(252)
    pdf.set_font('TimesNR', 'B', 9.0)
    pdf.cell(0, 4.5, "CORE PLATFORM & FRAMEWORK SPECIFICATIONS", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('TimesNR', '', 8.5)
    pdf.cell(0, 4.0, "• Database Engine: PostgreSQL 16   • Backend: Python 3.11   • UI Framework: Streamlit   • Data: Pandas & Plotly", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('TimesNR', 'I', 8.0)
    pdf.cell(0, 4.0, "Comprehensive Semester Report | Monochrome Edition | November 2026", align='C', new_x="LMARGIN", new_y="NEXT")


    # =========================================================================
    # PAGE 2: SECTIONS 1, 2 & 3 (BULLET POINTS)
    # =========================================================================
    pdf.add_page()
    pdf.set_y(22)
    
    pdf.chapter_heading("1", "Introduction and Project Overview")
    pdf.section_heading("1.1 Domain Motivation and Context")
    pdf.bullet("Data Intensity of Cricket", "Every professional cricket match generates a cascade of discrete events (balls bowled, runs scored, extras, bowling dismissals, and over-by-over run rates).")
    pdf.bullet("Limitations of Conventional Media", "Traditional portals display match scores as pre-formatted, static scorecard texts, which prevents ad-hoc querying, historical trend exploration, or cross-entity analysis.")
    pdf.bullet("DBMS-Driven Solution", "This project applies formal relational database principles to structure cricket operations into a normalized, queryable schema, preserving ACID properties and referential integrity.")
    pdf.bullet("Integrated Analytics Portal", "A Python and Streamlit web application connects directly to PostgreSQL, allowing users to browse fixtures, query career dossiers, and inspect interactive visualizations.")

    pdf.chapter_heading("2", "Objectives and Scope")
    pdf.section_heading("2.1 Core Engineering Objectives")
    pdf.bullet("3NF Schema Normalization", "Decompose cricket operations into nine normalized tables to eliminate update anomalies, data redundancy, and inconsistent recording.")
    pdf.bullet("Server-Side Business Rules", "Enforce domain constraints directly in PostgreSQL using declarative CHECK constraints, composite unique indexes, and four PL/pgSQL triggers.")
    pdf.bullet("Performant Query Abstraction", "Implement ten analytical SQL views and parameterized queries to derive batting averages, strike rates, and bowling economies with minimal application overhead.")
    pdf.bullet("Zero-JavaScript Web Dashboard", "Construct an intuitive, responsive Streamlit user interface featuring multi-entity search, interactive scorecards, and Plotly visualizations.")

    pdf.section_heading("2.2 System Boundaries & User Personas")
    pdf.bullet("Target Beneficiaries", "Coaches assessing player form; analysts tracking team strategies; students examining real-world relational database architectures.")
    pdf.bullet("Project Scope", "Encompasses completed limited-overs fixtures (IPL 2024–2025 dataset) across 10 franchises, 60 players, 8 stadiums, and 135 discrete deliveries.")
    pdf.bullet("Boundary Constraints", "Excludes spatial sensor tracking (Hawk-Eye pitch coordinates and wagon wheel angles) due to the absence of public coordinate telemetry APIs.")

    pdf.chapter_heading("3", "Technology Stack")
    pdf.section_heading("3.1 Technology Role and Selection Factors")
    
    tech_headers = ["Technology", "System Role", "Key Architectural Selection Factors"]
    tech_data = [
        ["PostgreSQL 16", "Relational Engine", "ACID compliance, procedural PL/pgSQL triggers, foreign key cascade/restrict rules, cost-based planner."],
        ["Python 3.11", "Application Backend", "Standard DB-API client (psycopg 3), parameterized query safety, vectorized data manipulation."],
        ["Streamlit", "Frontend Interface", "Python-native reactive UI, eliminating JavaScript build overhead while maintaining session state routing."],
        ["Pandas 2.0", "Tabular Structuring", "Vectorized transformations, group-by aggregations, and seamless translation of SQL cursor records."],
        ["Plotly Express", "Visual Analytics", "Publication-grade interactive charts (bars, donuts, scatter plots) with responsive hover tooltips."]
    ]
    pdf.render_table(tech_headers, tech_data, [26, 38, 116])


    # =========================================================================
    # PAGE 3: SECTIONS 4 & 5 (BULLET POINTS & SCHEMA DICTIONARY)
    # =========================================================================
    pdf.add_page()
    pdf.set_y(22)
    
    pdf.chapter_heading("4", "System Architecture and Data Flow")
    pdf.section_heading("4.1 Tiered Operational Pipeline")
    pdf.bullet("Storage Tier (PostgreSQL)", "Manages nine core tables, referential constraints, four business triggers, and ten analytical views.")
    pdf.bullet("Data Access Tier (Python/psycopg)", "Executes parameterized SQL queries via connection pooling with a 60-second in-memory cache for fast UI response.")
    pdf.bullet("Presentation Tier (Streamlit)", "Handles user input, manages session state routing, and dynamically renders metrics, scorecards, and Plotly charts.")

    pdf.chapter_heading("5", "Database Design: Entity Specifications")
    pdf.section_heading("5.1 Relational Schema Dictionary (Nine Tables, ~515 Records)")
    
    schema_headers = ["Table Name", "Primary Key", "Foreign Keys", "Attributes, Types & Integrity Constraints"]
    schema_data = [
        ["TEAMS", "team_id (INT)", "None", "team_name (VARCHAR(100), UQ, NOT NULL), country (VARCHAR(50)), coach (VARCHAR(100)). Stores franchise masters."],
        ["PLAYERS", "player_id (INT)", "team_id -> TEAMS", "full_name, date_of_birth (DATE), role (CHECK: batter, bowler, all-rounder, wicketkeeper), batting_style, bowling_style."],
        ["VENUES", "venue_id (INT)", "None", "venue_name (VARCHAR(100)), city (VARCHAR(50)), country (VARCHAR(50)), capacity (INT, CHECK > 0)."],
        ["MATCHES", "match_id (INT)", "home_team_id, away_team_id, venue_id", "match_date (DATE), match_format (CHECK: T20, ODI, Test), result_summary. CHECK: home_team_id <> away_team_id."],
        ["INNINGS", "innings_id (INT)", "match_id, batting_team_id", "innings_number (CHECK: 1, 2), total_runs (>=0), wickets_lost (0..10), overs_played, balls_bowled. UQ: (match_id, innings_number)."],
        ["BATTING_PERF", "batting_id (INT)", "innings_id, player_id", "runs_scored (>=0), balls_faced (>=0), fours, sixes, dismissal, not_out (BOOL), batting_position (1..11). UQ: (innings_id, player_id)."],
        ["BOWLING_PERF", "bowling_id (INT)", "innings_id, player_id", "overs_bowled (NUMERIC(3,1)), balls_bowled, maidens, runs_conceded (>=0), wickets_taken (>=0). UQ: (innings_id, player_id)."],
        ["FIELDING_PERF", "fielding_id (INT)", "innings_id, player_id", "catches (SMALLINT), stumpings (SMALLINT), run_outs (SMALLINT). UQ: (innings_id, player_id)."],
        ["DELIVERIES", "delivery_id (INT)", "innings_id, striker_id, bowler_id", "over_number (>=1), ball_number (1..6), runs_batter, extras, total_runs, wicket_type. UQ: (innings_id, over, ball). CHECK: striker <> bowler."]
    ]
    pdf.render_table(schema_headers, schema_data, [30, 26, 42, 82])

    pdf.section_heading("5.2 Key Strategy and Constraints")
    pdf.bullet("Surrogate Primary Keys", "Every table utilizes an auto-incrementing SERIAL integer primary key, optimizing B-tree index traversal and reducing foreign key storage footprint.")
    pdf.bullet("Natural Candidate Keys", "Enforced via composite UNIQUE constraints: (match_id, innings_number) in INNINGS; (innings_id, player_id) in performance tables; and (innings_id, over_number, ball_number) in DELIVERIES.")
    pdf.bullet("Domain Integrity Checks", "CHECK constraints guarantee realistic boundaries: capacity > 0; home_team_id <> away_team_id; innings_number IN (1, 2); and striker_id <> bowler_id.")


    # =========================================================================
    # PAGE 4: SECTION 6 (NORMALIZATION & INTEGRITY - BULLET POINTS)
    # =========================================================================
    pdf.add_page()
    pdf.set_y(22)
    
    pdf.chapter_heading("6", "Normalization and Integrity Constraints")
    pdf.section_heading("6.1 Formal Normalization Analysis (1NF to 3NF)")
    pdf.bullet("First Normal Form (1NF) Compliance", "All attributes are atomic and indivisible. Multi-valued elements (such as multiple overs bowled by a player or multiple boundaries) are stored as separate tuples in normalized tables, avoiding comma-separated strings or nested arrays.")
    pdf.bullet("Second Normal Form (2NF) Compliance", "The schema is in 1NF and contains zero partial functional dependencies. In composite candidate keys like (innings_id, player_id), every non-key attribute (e.g. runs_scored, overs_bowled) depends functionally on the entire composite key, not on any single component.")
    pdf.bullet("Third Normal Form (3NF) Compliance", "The schema is in 2NF and contains zero transitive functional dependencies (X -> Y -> Z). Player biographical attributes (full_name, date_of_birth, role, styles) depend exclusively on player_id in PLAYERS; performance records reference only player_id, eliminating redundant personal data across matches.")

    pdf.section_heading("6.2 Relational Integrity Constraints")
    pdf.bullet("Entity Integrity", "Every relation defines a NOT NULL, unique PRIMARY KEY enforced via an underlying B-tree index, guaranteeing that every row is distinctly identifiable.")
    pdf.bullet("Referential Integrity", "Foreign key constraints establish valid associations across parent and child relations, backed by strict deletion policies:")
    pdf.sub_bullet("ON DELETE RESTRICT Policy", "Applied to master entities (TEAMS, VENUES) referenced by MATCHES. The engine prevents dropping a stadium or franchise that is associated with recorded fixtures.")
    pdf.sub_bullet("ON DELETE CASCADE Policy", "Applied to hierarchical telemetry tables (INNINGS, DELIVERIES, BATTING_PERFORMANCE, BOWLING_PERFORMANCE, FIELDING_PERFORMANCE). Deleting a fixture cleanly purges all child innings and deliveries atomically.")
    pdf.sub_bullet("ON DELETE SET NULL Policy", "Configured on PLAYERS.team_id, permitting an athlete to become a free agent or change rosters without deleting their historical performance telemetry.")
    pdf.bullet("Domain Constraints & CHECK Rules", "Engine-level rules validate allowable data values:")
    pdf.sub_bullet("Stadium Capacity Validation", "capacity > 0 ensures stadium spectator counts are strictly positive.")
    pdf.sub_bullet("Fixture Integrity", "CHECK (home_team_id <> away_team_id) prevents a franchise from scheduling a fixture against itself.")
    pdf.sub_bullet("Delivery Participants", "CHECK (striker_id <> bowler_id) ensures the batter facing a ball cannot simultaneously be the bowler delivering it.")


    # =========================================================================
    # PAGE 5: SECTION 7 (RELATIONSHIPS, CARDINALITY & PARTICIPATION - BULLETS)
    # =========================================================================
    pdf.add_page()
    pdf.set_y(22)
    
    pdf.chapter_heading("7", "Relationships, Cardinality, and Participation Constraints")
    pdf.section_heading("7.1 Formal Definitions of Cardinality and Participation")
    pdf.bullet("Mapping Cardinality", "Defines the maximum number of entity instances in one set that can be associated with entity instances in another set (1:1, 1:N, or M:N).")
    pdf.bullet("Participation Constraints", "Specifies the minimum number of entity instances required in an association:")
    pdf.sub_bullet("Total Participation (Mandatory, 1..N / 1..1)", "Every instance in the entity set must participate in the relationship. Denoted by a double line or mandatory crossbar.")
    pdf.sub_bullet("Partial Participation (Optional, 0..N / 0..1)", "Instances may exist independently without participating in the relationship. Denoted by a single line or open circle.")

    pdf.section_heading("7.2 Comprehensive Relationship & Participation Matrix")
    rel_headers = ["Relationship Name", "Source", "Target", "Card.", "Source Part.", "Target Part.", "Foreign Key & Semantic Rules"]
    rel_data = [
        ["Hosted At", "VENUES", "MATCHES", "1 : N", "Partial (0..N)", "Total (1..1)", "MATCHES.venue_id (Venue may host 0 matches; match must have 1 venue)"],
        ["Contracts", "TEAMS", "PLAYERS", "1 : N", "Partial (0..N)", "Partial (0..1)", "PLAYERS.team_id (Team has 0..N players; player may be unassigned)"],
        ["Home Team", "TEAMS", "MATCHES", "1 : N", "Partial (0..N)", "Total (1..1)", "MATCHES.home_team_id (Team plays 0..N home games; match requires 1 home team)"],
        ["Away Team", "TEAMS", "MATCHES", "1 : N", "Partial (0..N)", "Total (1..1)", "MATCHES.away_team_id (Team plays 0..N away games; match requires 1 away team)"],
        ["Innings Of", "MATCHES", "INNINGS", "1 : 2", "Total (2..2)", "Total (1..1)", "INNINGS.match_id (Completed match has exactly 2 innings; innings links to 1 match)"],
        ["Bats In", "TEAMS", "INNINGS", "1 : N", "Partial (0..N)", "Total (1..1)", "INNINGS.batting_team_id (Team bats in 0..N innings; innings must have 1 batting team)"],
        ["Batting Perf.", "INNINGS", "PLAYERS", "M : N", "Total (1..11)", "Partial (0..N)", "Via BATTING_PERFORMANCE (innings has 1..11 batters; player bats in 0..N)"],
        ["Bowling Perf.", "INNINGS", "PLAYERS", "M : N", "Total (1..N)", "Partial (0..N)", "Via BOWLING_PERFORMANCE (innings has 1..N bowlers; player bowls in 0..N)"],
        ["Fielding Perf.", "INNINGS", "PLAYERS", "M : N", "Partial (0..N)", "Partial (0..N)", "Via FIELDING_PERFORMANCE (innings has 0..N catchers; player fields in 0..N)"],
        ["Ball Telemetry", "INNINGS", "DELIVERIES", "1 : N", "Partial (0..120)", "Total (1..1)", "DELIVERIES.innings_id (Innings has up to 120 balls; delivery belongs to 1 innings)"],
        ["Ball Striker", "PLAYERS", "DELIVERIES", "1 : N", "Partial (0..N)", "Total (1..1)", "DELIVERIES.striker_id (Player faces 0..N deliveries; delivery must have 1 striker)"],
        ["Ball Bowler", "PLAYERS", "DELIVERIES", "1 : N", "Partial (0..N)", "Total (1..1)", "DELIVERIES.bowler_id (Player delivers 0..N balls; delivery must have 1 bowler)"]
    ]
    pdf.render_table(rel_headers, rel_data, [22, 22, 22, 14, 20, 20, 60])

    pdf.section_heading("7.3 Resolution of Many-to-Many Relationships")
    pdf.bullet("The M:N Association Problem", "Players participate in multiple matches, and each match involves 22 athletes. Directly associating PLAYERS and INNINGS would produce redundant multi-valued tuples and sparse null fields.")
    pdf.bullet("Decomposition into Three Junction Tables", "The M:N relationship is resolved into three specialized entities: BATTING_PERFORMANCE, BOWLING_PERFORMANCE, and FIELDING_PERFORMANCE. Each records distinct metrics (runs, overs, catches) with its own surrogate PK and composite candidate key.")


    # =========================================================================
    # PAGE 6: SECTION 8 (ER DIAGRAM & BULLET WALKTHROUGH)
    # =========================================================================
    pdf.add_page()
    pdf.set_y(22)
    
    pdf.chapter_heading("8", "Entity Relationship (ER) Diagram")
    pdf.section_heading("8.1 Diagrammatic Representation (Crow's Foot Notation)")
    pdf.bullet("Formal ER Architecture", "The diagram below illustrates the nine relational tables, primary keys, foreign keys, constraints, and cardinalities in standard monochrome Crow's Foot notation.")

    # Embed High-Resolution Monochrome ER Diagram
    er_image_path = "database_documentation/Cricket_Analytics_ER_Diagram.png"
    if os.path.exists(er_image_path):
        img_y = pdf.get_y() + 1
        pdf.image(er_image_path, x=15, y=img_y, w=180, h=118)
        pdf.set_y(img_y + 120)

    pdf.section_heading("8.2 Structural Walkthrough of Diagram Connectors")
    pdf.bullet("VENUE to MATCHES Connector", "Mandatory One crossbars at VENUES (every match requires exactly one venue); Optional Many fork at MATCHES (a venue can exist before hosting matches).")
    pdf.bullet("TEAM to MATCHES Dual Connectors", "Two independent 1:N relations (home_team_id, away_team_id). Both are Total for MATCHES, ensuring valid participant franchises for every fixture.")
    pdf.bullet("MATCHES to INNINGS Composition", "Mandatory 1:2 relationship. Exactly two sequential innings exist for every completed limited-overs match, governed by UNIQUE (match_id, innings_number).")
    pdf.bullet("Performance Junction Connectors", "INNINGS and PLAYERS connect to BATTING_PERFORMANCE, BOWLING_PERFORMANCE, and FIELDING_PERFORMANCE through 1:N links, ensuring independent recording of distinct athletic disciplines.")


    # =========================================================================
    # PAGE 7: SECTIONS 9 & 10 (TRIGGERS, VIEWS, IMPLEMENTATION - BULLETS)
    # =========================================================================
    pdf.add_page()
    pdf.set_y(22)
    
    pdf.chapter_heading("9", "Procedural Logic & Analytical Abstractions")
    pdf.section_heading("9.1 PL/pgSQL Domain Triggers")
    pdf.bullet("Trigger 1: trg_set_delivery_total", "Runs BEFORE INSERT OR UPDATE on DELIVERIES. Computes NEW.total_runs := COALESCE(NEW.runs_batter, 0) + COALESCE(NEW.extras, 0). Eliminates run arithmetic discrepancies.")
    pdf.bullet("Trigger 2: trg_validate_overs_format", "Runs BEFORE INSERT OR UPDATE on BOWLING_PERFORMANCE. Validates that the decimal part of overs_bowled is between .0 and .5. Throws an exception if .6 through .9 is entered, directly enforcing the 6-balls-per-over rule.")
    pdf.bullet("Trigger 3: trg_sync_batting_not_out", "Runs BEFORE INSERT OR UPDATE on BATTING_PERFORMANCE. Automatically forces not_out = TRUE if dismissal is 'not out', and toggles not_out = FALSE when a dismissal method is recorded.")
    pdf.bullet("Trigger 4: trg_validate_player_age", "Runs BEFORE INSERT OR UPDATE on PLAYERS. Enforces date_of_birth <= CURRENT_DATE - INTERVAL '15 years', preventing the registration of invalid dates or underage athletes.")

    pdf.section_heading("9.2 Pre-Aggregated Relational Views")
    pdf.bullet("TOP_RUN_SCORERS View", "Aggregates career innings, runs, highest scores, centuries, fifties, batting strike rates, and batting averages.")
    pdf.bullet("TOP_WICKET_TAKERS View", "Calculates total wickets, overs bowled, maidens, runs conceded, bowling economy rates, and bowling averages.")
    pdf.bullet("TEAM_PERFORMANCE View", "Computes tournament standings: matches played, wins, losses, win percentage, and total runs scored/conceded.")
    pdf.bullet("MATCH_SCORECARD View", "Provides unified match sheets joining teams, venues, innings totals, and match results.")
    pdf.bullet("VENUE_STATISTICS View", "Analyzes venue utilization, average first-innings totals, and toss-winner match outcomes.")

    pdf.chapter_heading("10", "Application Implementation and Query Processing")
    pdf.section_heading("10.1 Data Access Layer and Parameterization")
    pdf.bullet("Parameterized Queries", "Database operations in database.py utilize psycopg 3 with %s placeholder bindings, preventing SQL injection vulnerabilities.")
    pdf.bullet("In-Memory Caching", "Queries are cached with Streamlit's @st.cache_data(ttl=60) decorator, providing snappy UI transitions while reflecting database updates within 60 seconds.")
    pdf.bullet("Deferred Navigation State Pattern", "Redirects between search chips, leaderboards, and profile pages via st.session_state target variables, eliminating widget key collisions.")


    # =========================================================================
    # PAGE 8: SECTIONS 11 & 12 (SQL SAMPLES, CONCLUSION, SIGN-OFF - BULLETS)
    # =========================================================================
    pdf.add_page()
    pdf.set_y(22)
    
    pdf.chapter_heading("11", "Representative SQL Query Operations")
    pdf.section_heading("11.1 Dynamic Batting Aggregate Query (from queries.py)")
    
    sql_sample_1 = (
        "SELECT p.player_id, p.full_name, t.team_name,\n"
        "       COUNT(bp.batting_id) AS innings_played,\n"
        "       SUM(bp.runs_scored) AS total_runs,\n"
        "       MAX(bp.runs_scored) AS highest_score,\n"
        "       ROUND(SUM(bp.runs_scored)::DECIMAL / NULLIF(SUM(CASE WHEN bp.not_out = FALSE THEN 1 ELSE 0 END), 0), 2) AS batting_avg,\n"
        "       ROUND((SUM(bp.runs_scored)::DECIMAL / NULLIF(SUM(bp.balls_faced), 0)) * 100, 2) AS strike_rate\n"
        "FROM PLAYERS p\n"
        "JOIN TEAMS t ON p.team_id = t.team_id\n"
        "JOIN BATTING_PERFORMANCE bp ON p.player_id = bp.player_id\n"
        "GROUP BY p.player_id, p.full_name, t.team_name\n"
        "ORDER BY total_runs DESC LIMIT 10;"
    )
    pdf.code_box(sql_sample_1, "Career Batting Aggregation with Dynamic Strike Rate")

    pdf.section_heading("11.2 Innings Bowling Figures Query")
    sql_sample_2 = (
        "SELECT bp.player_id, p.full_name, bp.overs_bowled, bp.maidens, bp.runs_conceded, bp.wickets_taken,\n"
        "       ROUND((bp.runs_conceded::DECIMAL / NULLIF(bp.overs_bowled, 0)), 2) AS economy_rate\n"
        "FROM BOWLING_PERFORMANCE bp\n"
        "JOIN PLAYERS p ON bp.player_id = p.player_id\n"
        "WHERE bp.innings_id = %s\n"
        "ORDER BY bp.wickets_taken DESC, economy_rate ASC;"
    )
    pdf.code_box(sql_sample_2, "Innings Bowling Extraction with Parameterized Filter")

    pdf.chapter_heading("12", "Conclusion and Future Enhancements")
    pdf.section_heading("12.1 Project Accomplishments & Technical Competencies")
    pdf.bullet("Relational Modeling Rigor", "Demonstrated end-to-end 3NF decomposition, eliminating update anomalies while preserving domain consistency.")
    pdf.bullet("Server-Side Automation", "Enforced business rules using declarative constraints and procedural PL/pgSQL triggers inside PostgreSQL.")
    pdf.bullet("Full-Stack Python Synergy", "Delivered a responsive web interface with zero JavaScript overhead, integrating psycopg, Pandas, and Plotly.")

    pdf.section_heading("12.2 Realistic Future Enhancements")
    pdf.bullet("Automated Ingestion Pipeline", "Build an automated ETL worker to ingest ball-by-ball JSON feeds directly from open-source repositories.")
    pdf.bullet("Predictive Machine Learning", "Integrate logistic regression models to compute live in-play win probabilities based on required run rates.")
    pdf.bullet("Spatial Telemetry Mapping", "Augment DELIVERIES with pitch landing coordinates (X, Y) and wagon wheel polar angles.")

    pdf.ln(1)
    # Verification Sign-off Box
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.4)
    pdf.rect(15, pdf.get_y(), 180, 20)
    pdf.set_y(pdf.get_y() + 2)
    pdf.set_font('TimesNR', 'B', 8.5)
    pdf.cell(0, 4.2, "ACADEMIC VERIFICATION & SIGN-OFF", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('TimesNR', '', 8.0)
    pdf.cell(0, 4.0, "• Verification: This project report and associated relational database represent authentic, verified student coursework.", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4.0, "• Database Engine: PostgreSQL 16 | Font: Times New Roman | Monochrome Edition (Bullet Structured)", align='C', new_x="LMARGIN", new_y="NEXT")

    output_pdf_path = "database_documentation/Cricket_Analytics_Project_Report.pdf"
    pdf.output(output_pdf_path)
    print(f"Generated Project Report PDF at: {output_pdf_path}")
    print(f"Total Pages Generated: {pdf.page_no()}")

if __name__ == "__main__":
    generate_report()

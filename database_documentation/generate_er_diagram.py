import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_er_diagram(output_path):
    fig, ax = plt.subplots(figsize=(24, 16), dpi=300)
    ax.set_xlim(0, 2400)
    ax.set_ylim(0, 1600)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title Banner (Black outline, white fill, black serif text)
    title_box = patches.Rectangle(
        (80, 1500), 2240, 70,
        linewidth=2, edgecolor='#000000', facecolor='#FFFFFF'
    )
    ax.add_patch(title_box)
    ax.text(1200, 1545, "CRICKET ANALYTICS DATABASE -- ENTITY RELATIONSHIP (ER) DIAGRAM",
            color='#000000', fontsize=18, fontweight='bold', ha='center', va='center', fontfamily='serif')
    ax.text(1200, 1515, "PostgreSQL Relational Schema (3NF) | Crow's Foot Notation | Cardinalities & Participation Constraints",
            color='#000000', fontsize=11, fontstyle='italic', ha='center', va='center', fontfamily='serif')

    # Legend at bottom
    legend_box = patches.Rectangle(
        (80, 25), 2240, 45,
        linewidth=1.2, edgecolor='#000000', facecolor='#FFFFFF'
    )
    ax.add_patch(legend_box)
    legend_text = (
        "NOTATION:   [PK] Primary Key   |   [FK] Foreign Key   |   [CK] Check Constraint   |   [UQ] Unique Constraint   |   "
        "--||-- Mandatory One (Total)   |   --|o-- Optional One (Partial)   |   --<|-- Mandatory Many   |   --<o-- Optional Many"
    )
    ax.text(1200, 47, legend_text, color='#000000', fontsize=10.5, fontweight='bold', ha='center', va='center', fontfamily='serif')

    # Table specifications
    tables = {
        'VENUES': {
            'pos': (100, 1140), 'size': (460, 280),
            'header': 'VENUES (Stadium Master)',
            'pk': ['venue_id : SERIAL [PK]'],
            'attrs': [
                'venue_name : VARCHAR(100) NOT NULL',
                'city : VARCHAR(50) NOT NULL',
                'country : VARCHAR(50) NOT NULL',
                'capacity : INT (CHECK capacity > 0)'
            ],
            'fks': []
        },
        'TEAMS': {
            'pos': (840, 1140), 'size': (480, 280),
            'header': 'TEAMS (Franchise Master)',
            'pk': ['team_id : SERIAL [PK]'],
            'attrs': [
                'team_name : VARCHAR(100) UNIQUE NOT NULL',
                'country : VARCHAR(50) NOT NULL',
                'coach : VARCHAR(100)'
            ],
            'fks': []
        },
        'PLAYERS': {
            'pos': (1620, 1100), 'size': (580, 340),
            'header': 'PLAYERS (Roster Details)',
            'pk': ['player_id : SERIAL [PK]'],
            'attrs': [
                'full_name : VARCHAR(100) NOT NULL',
                'date_of_birth : DATE NOT NULL',
                'role : VARCHAR(20) NOT NULL [CK]',
                'batting_style : VARCHAR(30)',
                'bowling_style : VARCHAR(30)'
            ],
            'fks': [
                'team_id : INT [FK -> TEAMS.team_id]'
            ]
        },
        'MATCHES': {
            'pos': (100, 600), 'size': (500, 380),
            'header': 'MATCHES (Fixture & Results)',
            'pk': ['match_id : SERIAL [PK]'],
            'attrs': [
                'match_date : DATE NOT NULL',
                'match_format : VARCHAR(10) NOT NULL [CK]',
                'result_summary : VARCHAR(255)',
                '[CK: home_team_id <> away_team_id]'
            ],
            'fks': [
                'home_team_id : INT [FK -> TEAMS.team_id]',
                'away_team_id : INT [FK -> TEAMS.team_id]',
                'venue_id : INT [FK -> VENUES.venue_id]'
            ]
        },
        'INNINGS': {
            'pos': (840, 600), 'size': (500, 380),
            'header': 'INNINGS (Match Breakdown)',
            'pk': ['innings_id : SERIAL [PK]'],
            'attrs': [
                'innings_number : SMALLINT (1 or 2) [CK]',
                'total_runs : INT DEFAULT 0 (>= 0)',
                'wickets_lost : SMALLINT (0 to 10)',
                'overs_played : NUMERIC(4,1) DEFAULT 0.0',
                'balls_bowled : INT DEFAULT 0',
                '[UQ: (match_id, innings_number)]'
            ],
            'fks': [
                'match_id : INT [FK -> MATCHES.match_id]',
                'batting_team_id : INT [FK -> TEAMS.team_id]'
            ]
        },
        'FIELDING_PERFORMANCE': {
            'pos': (1640, 640), 'size': (540, 300),
            'header': 'FIELDING_PERFORMANCE (Junction)',
            'pk': ['fielding_id : SERIAL [PK]'],
            'attrs': [
                'catches : SMALLINT DEFAULT 0',
                'stumpings : SMALLINT DEFAULT 0',
                'run_outs : SMALLINT DEFAULT 0',
                '[UQ: (innings_id, player_id)]'
            ],
            'fks': [
                'innings_id : INT [FK -> INNINGS.innings_id]',
                'player_id : INT [FK -> PLAYERS.player_id]'
            ]
        },
        'DELIVERIES': {
            'pos': (100, 110), 'size': (540, 390),
            'header': 'DELIVERIES (Ball-by-Ball Telemetry)',
            'pk': ['delivery_id : SERIAL [PK]'],
            'attrs': [
                'over_number : SMALLINT (>= 1)',
                'ball_number : SMALLINT (1 to 6)',
                'runs_batter : SMALLINT DEFAULT 0',
                'extras : SMALLINT DEFAULT 0',
                'total_runs : SMALLINT DEFAULT 0 [TRG]',
                'wicket_type : VARCHAR(30)',
                '[UQ: (innings_id, over_number, ball_number)]',
                '[CK: striker_id <> bowler_id]'
            ],
            'fks': [
                'innings_id : INT [FK -> INNINGS.innings_id]',
                'striker_id : INT [FK -> PLAYERS.player_id]',
                'bowler_id : INT [FK -> PLAYERS.player_id]'
            ]
        },
        'BOWLING_PERFORMANCE': {
            'pos': (840, 110), 'size': (540, 390),
            'header': 'BOWLING_PERFORMANCE (Junction)',
            'pk': ['bowling_id : SERIAL [PK]'],
            'attrs': [
                'overs_bowled : NUMERIC(3,1) DEFAULT 0.0',
                'balls_bowled : INT DEFAULT 0',
                'maidens : SMALLINT DEFAULT 0',
                'runs_conceded : INT DEFAULT 0',
                'wickets_taken : SMALLINT DEFAULT 0',
                '[UQ: (innings_id, player_id)]'
            ],
            'fks': [
                'innings_id : INT [FK -> INNINGS.innings_id]',
                'player_id : INT [FK -> PLAYERS.player_id]'
            ]
        },
        'BATTING_PERFORMANCE': {
            'pos': (1640, 110), 'size': (540, 420),
            'header': 'BATTING_PERFORMANCE (Junction)',
            'pk': ['batting_id : SERIAL [PK]'],
            'attrs': [
                'runs_scored : INT DEFAULT 0',
                'balls_faced : INT DEFAULT 0',
                'fours : INT DEFAULT 0',
                'sixes : INT DEFAULT 0',
                'dismissal : VARCHAR(100) DEFAULT \'not out\'',
                'not_out : BOOLEAN DEFAULT TRUE [TRG]',
                'batting_position : SMALLINT (1 to 11)',
                '[UQ: (innings_id, player_id)]'
            ],
            'fks': [
                'innings_id : INT [FK -> INNINGS.innings_id]',
                'player_id : INT [FK -> PLAYERS.player_id]'
            ]
        }
    }

    # Render table in monochrome academic style
    def render_table(t_name, data):
        x, y = data['pos']
        w, h = data['size']
        header_h = 40

        # Outer border
        main_box = patches.Rectangle(
            (x, y), w, h,
            linewidth=1.5, edgecolor='#000000', facecolor='#FFFFFF'
        )
        ax.add_patch(main_box)

        # Header box (light gray tint for distinction, solid black border)
        header_box = patches.Rectangle(
            (x, y + h - header_h), w, header_h,
            linewidth=1.2, edgecolor='#000000', facecolor='#F2F2F2'
        )
        ax.add_patch(header_box)

        # Header text (Black bold serif)
        ax.text(x + 16, y + h - (header_h / 2), data['header'],
                color='#000000', fontsize=11.5, fontweight='bold', va='center', fontfamily='serif')

        curr_y = y + h - header_h - 22
        
        # Primary Keys
        for pk in data['pk']:
            ax.text(x + 18, curr_y + 4, "[PK]", color='#000000', fontsize=9.5, fontweight='bold', va='center', fontfamily='serif')
            ax.text(x + 55, curr_y + 4, pk.replace(" [PK]", ""), color='#000000', fontsize=10, fontweight='bold', va='center', fontfamily='serif')
            curr_y -= 24

        # Divider line
        ax.plot([x, x + w], [curr_y + 12, curr_y + 12], color='#000000', linewidth=1)

        # Foreign Keys
        for fk in data['fks']:
            ax.text(x + 18, curr_y + 4, "[FK]", color='#000000', fontsize=9.5, fontweight='bold', va='center', fontfamily='serif')
            ax.text(x + 55, curr_y + 4, fk.replace(" [FK]", ""), color='#000000', fontsize=9.5, va='center', fontfamily='serif')
            curr_y -= 24

        if data['fks']:
            ax.plot([x, x + w], [curr_y + 12, curr_y + 12], color='#777777', linewidth=0.8, linestyle='--')

        # Regular Attributes & Constraints
        for attr in data['attrs']:
            is_ck = "[CK" in attr or "[UQ" in attr or "[TRG]" in attr
            weight = 'normal'
            font_size = 9 if is_ck else 9.5
            prefix = " " if is_ck else "- "
            ax.text(x + 18, curr_y + 4, f"{prefix}{attr}", color='#000000', fontsize=font_size, fontweight=weight, va='center', fontfamily='serif')
            curr_y -= 22

    for t_name, data in tables.items():
        render_table(t_name, data)

    # Function to draw Crow's Foot connector lines in black
    def draw_crows_foot(x1, y1, x2, y2, label="", points=None, style='-'):
        if points is None:
            points = [(x1, y1), (x2, y2)]
        
        px = [p[0] for p in points]
        py = [p[1] for p in points]
        ax.plot(px, py, color='#000000', linewidth=1.8, linestyle=style, zorder=3)

        # Draw One-and-only-one on (x1, y1)
        dx1 = points[1][0] - points[0][0]
        dy1 = points[1][1] - points[0][1]
        dist1 = (dx1**2 + dy1**2)**0.5
        if dist1 > 0:
            ux1, uy1 = dx1/dist1, dy1/dist1
            nx1, ny1 = -uy1, ux1
            for offset in [8, 16]:
                cx = points[0][0] + ux1 * offset
                cy = points[0][1] + uy1 * offset
                ax.plot([cx - nx1*8, cx + nx1*8], [cy - ny1*8, cy + ny1*8], color='#000000', linewidth=1.8, zorder=4)

        # Draw Crow's Foot on (x2, y2)
        dx2 = points[-1][0] - points[-2][0]
        dy2 = points[-1][1] - points[-2][1]
        dist2 = (dx2**2 + dy2**2)**0.5
        if dist2 > 0:
            ux2, uy2 = dx2/dist2, dy2/dist2
            nx2, ny2 = -uy2, ux2
            fx, fy = points[-1][0], points[-1][1]
            bx = fx - ux2 * 18
            by = fy - uy2 * 18
            ax.plot([bx + nx2*12, fx], [by + ny2*12, fy], color='#000000', linewidth=1.8, zorder=4)
            ax.plot([bx - nx2*12, fx], [by - ny2*12, fy], color='#000000', linewidth=1.8, zorder=4)
            cx = bx - ux2 * 6
            cy = by - uy2 * 6
            ax.plot([cx - nx2*8, cx + nx2*8], [cy - ny2*8, cy + ny2*8], color='#000000', linewidth=1.8, zorder=4)

        # Label box
        if label:
            mid_idx = len(points) // 2
            lx = (points[mid_idx-1][0] + points[mid_idx][0]) / 2
            ly = (points[mid_idx-1][1] + points[mid_idx][1]) / 2
            lbl_box = patches.Rectangle(
                (lx - 75, ly - 10), 150, 20,
                linewidth=1, edgecolor='#000000', facecolor='#FFFFFF', zorder=5
            )
            ax.add_patch(lbl_box)
            ax.text(lx, ly, label, color='#000000', fontsize=8.5, fontweight='bold', ha='center', va='center', fontfamily='serif', zorder=6)

    # 1. VENUES (1) -> MATCHES (N)
    draw_crows_foot(330, 1140, 330, 980, label="1 (M) : N (O) [hosted at]")

    # 2. TEAMS (1) -> PLAYERS (N)
    draw_crows_foot(1320, 1280, 1620, 1280, label="1 (M) : N (O) [contracts]")

    # 3. TEAMS (1) -> MATCHES (N)
    draw_crows_foot(
        840, 1260, 600, 940,
        points=[(840, 1260), (700, 1260), (700, 940), (600, 940)],
        label="1 (M) : N (O) [home/away]"
    )

    # 4. TEAMS (1) -> INNINGS (N)
    draw_crows_foot(1080, 1140, 1080, 980, label="1 (M) : N (O) [bats in]")

    # 5. MATCHES (1) -> INNINGS (2)
    draw_crows_foot(600, 790, 840, 790, label="1 (M) : 2 (M) [innings of]")

    # 6. INNINGS (1) -> FIELDING_PERFORMANCE (N)
    draw_crows_foot(1340, 790, 1640, 790, label="1 (M) : N (O) [fielding]")

    # 7. PLAYERS (1) -> FIELDING_PERFORMANCE (N)
    draw_crows_foot(1910, 1100, 1910, 940, label="1 (M) : N (O) [fields]")

    # 8. INNINGS (1) -> BOWLING_PERFORMANCE (N)
    draw_crows_foot(1100, 600, 1100, 500, label="1 (M) : N (O) [bowling]")

    # 9. PLAYERS (1) -> BOWLING_PERFORMANCE (N)
    draw_crows_foot(
        1750, 1100, 1380, 420,
        points=[(1750, 1100), (1750, 1020), (1450, 1020), (1450, 420), (1380, 420)],
        label="1 (M) : N (O) [bowls]"
    )

    # 10. INNINGS (1) -> BATTING_PERFORMANCE (N)
    draw_crows_foot(
        1340, 680, 1640, 440,
        points=[(1340, 680), (1520, 680), (1520, 440), (1640, 440)],
        label="1 (M) : N (O) [batting]"
    )

    # 11. PLAYERS (1) -> BATTING_PERFORMANCE (N)
    draw_crows_foot(2050, 1100, 2050, 530, label="1 (M) : N (O) [bats]")

    # 12. INNINGS (1) -> DELIVERIES (N)
    draw_crows_foot(
        840, 680, 640, 420,
        points=[(840, 680), (740, 680), (740, 420), (640, 420)],
        label="1 (M) : N (O) [balls]"
    )

    # 13. PLAYERS (1) -> DELIVERIES (N)
    draw_crows_foot(
        1620, 1350, 370, 500,
        points=[(1620, 1350), (1400, 1450), (680, 1450), (40, 1450), (40, 530), (370, 530), (370, 500)],
        label="1 (M) : N (O) [striker/bowler]",
        style='--'
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='#FFFFFF', edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated monochrome academic ER Diagram at: {output_path}")

if __name__ == "__main__":
    draw_er_diagram("database_documentation/Cricket_Analytics_ER_Diagram.png")


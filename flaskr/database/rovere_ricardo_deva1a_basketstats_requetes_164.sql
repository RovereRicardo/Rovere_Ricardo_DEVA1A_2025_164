-- Insérer un nouvel utilisateur
INSERT INTO t_user (id_user,username, name, email, password, role)
VALUES (1500,'requete', 'Mr Requete', 'requete@example.com', 'requetemdp', 'coach');


-- Créer une nouvelle équipe avec le coach d'id 1500
INSERT INTO t_team (id_team, team_name, address, city, wins, loses, matches_played, points, id_coach_creator)
VALUES (2000,'DreamTeam Requetes', 'Rue des Requetes 123', 'RequeteCity', 10, 2, 12, 32, 1500);

-- Ajouter un nouveau joueur
INSERT INTO t_player (id_player, name, family_name, number, position_name, height, birthday, nationality)
VALUES (3000,'Manuelito', 'Requetito', 7, 'ATK', 180, '2000-06-15', 'MX');

-- Associer le joueur à l'équipe 2000
INSERT INTO t_team_player (id_team_player, id_player_team)
VALUES (2000, 3000);

-- Planifier un match entre l’équipe 75 et l’équipe 2000
INSERT INTO t_match (id_home_team, id_away_team, date_match)
VALUES (75, 2000, '2025-06-10');

-- Indiquer que le joueur a participé au match
INSERT INTO t_players_match (id_match, id_player, subbed, played)
VALUES (1500, 3000, 0, 1);

-- Obtenir tous les joueurs de l'équipe 76
SELECT p.*
FROM t_player p
JOIN t_team_player tp ON p.id_player = tp.id_player_team
WHERE tp.id_team_player = 76;

-- Obtenir les détails des résultats des matchs joués
SELECT m.id_match, home.team_name AS equipe_domicile, away.team_name AS equipe_exterieure, m.home_score, m.away_score
FROM t_match m
JOIN t_team home ON m.id_home_team = home.id_team
JOIN t_team away ON m.id_away_team = away.id_team
WHERE m.is_played = 1;

-- Lister toutes les statistiques d’un joueur donné
SELECT s.id_match, st.name AS nom_statistique, s.value
FROM t_stats s
JOIN t_stats_type st ON s.id_stat_type = st.id
WHERE s.id_player = 60;

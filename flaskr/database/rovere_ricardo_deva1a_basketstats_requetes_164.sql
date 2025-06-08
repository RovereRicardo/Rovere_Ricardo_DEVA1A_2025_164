-- Insérer un nouvel utilisateur
INSERT INTO t_user (username, name, email, password, role)
VALUES ('requete', 'Mr Requete', 'requete@example.com', 'requetemdp', 'coach');


-- Créer une nouvelle équipe avec le coach d'id 1
INSERT INTO t_team (id_team, team_name, address, city, wins, loses, matches_played, points, id_coach_creator)
VALUES (2000,'DreamTeam Requetes', 'Rue des Requetes 123', 'RequeteCity', 10, 2, 12, 32, 1500);

-- Ajouter un nouveau joueur
INSERT INTO t_player (id_player, name, family_name, number, position_name, height, birthday, nationality)
VALUES (3000,'Manuelito', 'Requetito', 7, 'ATK', 180, '2000-06-15', 'MX');

-- Associer le joueur à l'équipe 1
INSERT INTO t_team_player (id_team_player, id_player_team)
VALUES (2000, 3000);

-- Planifier un match entre l’équipe 1 et l’équipe 2
INSERT INTO t_match (id_home_team, id_away_team, date_match)
VALUES (1, 2000, '2025-06-10');

-- Indiquer que le joueur a participé au match
INSERT INTO t_players_match (id_match, id_player, subbed, played)
VALUES (1500, 3000, 0, 1);

-- Obtenir tous les joueurs de l'équipe 1
SELECT p.*
FROM t_player p
JOIN t_team_player tp ON p.id_player = tp.id_player_team
WHERE tp.id_team_player = 1;

-- Obtenir les détails des résultats des matchs joués
SELECT m.id_match, ht.team_name AS equipe_domicile, at.team_name AS equipe_exterieure, m.home_score, m.away_score
FROM t_match m
JOIN t_team ht ON m.id_home_team = ht.id_team
JOIN t_team at ON m.id_away_team = at.id_team
WHERE m.is_played = 1;

-- Lister toutes les statistiques d’un joueur donné
SELECT s.id_match, st.name AS nom_statistique, s.value
FROM t_stats s
JOIN t_stats_type st ON s.id_stat_type = st.id
WHERE s.id_player = 1;

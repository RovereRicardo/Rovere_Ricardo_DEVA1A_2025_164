SELECT p.name, p.family_name, pm.id_match
FROM t_player p
LEFT JOIN t_players_match pm ON p.id_player = pm.id_player;


SELECT m.id_match, m.date_match, ht.team_name AS home_team_name
FROM t_match m
LEFT JOIN t_team ht ON m.id_home_team = ht.id_team;

INSERT INTO `t_player` (`id_player`, `name`, `family_name`, `picture`, `number`, `position`, `position_name`, `height`, `birthday`, `nationality`, `is_deleted`) VALUES
(200, 'Requetes', 'Requete', NULL, 20, 2, 'SG', 183, '1990-02-20', 'CH', 0)

UPDATE t_player SET name = "Update" WHERE id_player = 200;

DELETE FROM t_player WHERE `t_player`.`id_player` = 200


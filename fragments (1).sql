DELETE FROM 'group';
DELETE FROM topic;
DELETE FROM topic_answer;
DELETE FROM topic_ticket;
DELETE FROM topic_item;
DELETE FROM user;
DELETE FROM user_group;

INSERT INTO "user"
(id_user, name_user,code_user, email_user, password_hash, password_salt,icon_user)
VALUES
(1, 'Marga Nacher','MNacher', 'marga@email.com', '$2b$12$gIcSbXQrWqMHTFhbcNOguOQhSNDDq.nQpuX25Fgfy4HKrrIScnaWm', '$2b$12$gIcSbXQrWqMHTFhbcNOguO',''),
(2, 'Gonzalo Pardo','GPardo', 'gonzalo@email.com', '$2b$12$6e2DSOJwq.Z/pz8LawWPH.WXj3mfkitZkS76ykL61NQy1cwOFYhCS', '$2b$12$6e2DSOJwq.Z/pz8LawWPH.',''),
(3, 'Jill Esteban','JEsteban', 'jill@email.com', '$2b$12$Sox8sFxljetZ41VEhcR2SOV8P2pD5dkyKjbFp0LZ6vzGLrb2kE/iu', '$2b$12$Sox8sFxljetZ41VEhcR2SO',''),
(4, 'Pedro Picapiedra','PPicapiedra', 'pedro@email.com', '$2b$12$Sox8sFxljetZ41VEhcR2SOV8P2pD5dkyKjbFp0LZ6vzGLrb2kE/iu', '$2b$12$Sox8sFxljetZ41VEhcR2SO','');

INSERT INTO "group"
(id_group, name_group,id_owner)
VALUES
(1, 'Group Sprint 16',1),
(2, 'Group Sprint 17',2),
(3, 'Group lunch',3),
(4, 'Group Team Leaders',3);


INSERT INTO user_group
(user_id, group_id)
VALUES
(1, 2),
(2, 1),
(1, 3),
(2, 3),
(2, 4),
(3, 4);

--status = 1 = active, status = 0 = inactive
INSERT INTO topic
(id_topic, title_topic, id_owner, type_topic, start_date, end_date, status, participation,deleted_date)
VALUES
(1, '♠A of ♠ - Consum Sprint 17', 1, 'AceOfSpadesTopic', '2023-04-20 00:00:00.000000', '2023-05-20 00:00:00.000000', True, 0,'9999-12-31 00:00:00.000000'),
(2, 'Rate Demo Sprint 16', 1, 'RatingTopic', '2023-04-18 00:00:00.000000', '2023-05-20 00:00:00.000000', True, 0,'9999-12-31 00:00:00.000000'),
(3, '♠A of ♠ - Consum Sprint 16', 2, 'AceOfSpadesTopic', '2023-04-01 00:00:00.000000', '2023-05-20 00:00:00.000000', True, 0,'9999-12-31 00:00:00.000000'),
(4, '¿Cuándo vamos a la Oficina?', 3, 'MultipleChoiceTextTopic', '2023-02-12 00:00:00.000000', '2023-05-20 00:00:00.000000', True, 0,'9999-12-31 00:00:00.000000');



-- 1 = completed, 0 = not completed
INSERT INTO topic_ticket
(user_id, topic_id, completed)
VALUES	  
(2, 1, 0),
(2, 2, 0),
(3, 2, 0),
(1, 3, 0),
(2, 4, 0),
(3, 4, 0);


INSERT INTO topic_item
(id_topic_item, id_topic, id_order, text_answers)
VALUES
(1, 1, 1, 'Paco'),
(2, 1, 2, 'Maria'),
(3, 1, 3, 'Ilse'),
(4, 3, 1, 'Paco'),
(5, 3, 2, 'Maria'),
(6, 3, 3, 'Ilse'),
(7, 4, 1, 'Lunes, Miercoles'),
(8, 4, 2, 'Martes, Jueves'),
(9, 4, 3, 'Una semana lu, mi, otra ma, jue'),
(10, 4, 4, 'Me da igual');

INSERT INTO topic_answer
(id_topic_answer, id_topic, answer)
VALUES
(1, 3, '3'),
(2, 3, '3'),
(3, 3, '2'),
(4, 3, '2'),
(5, 1, '3');


--INSERT INTO user_topic
(--topic_id, user_id)
--VALUES
--(1, 2),
--(2, 2),
--(3, 2),
--(1, 1),
--(2, 1),
--(3, 1),
--(4, 1);

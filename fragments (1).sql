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
(1, 'Laura Gordo','LGordo', 'lgordo@email.com', '$2b$12$gIcSbXQrWqMHTFhbcNOguOQhSNDDq.nQpuX25Fgfy4HKrrIScnaWm', '$2b$12$gIcSbXQrWqMHTFhbcNOguO',''),
(2, 'Pilar Lapayese','PLapayese', 'plapayese@email.com', '$2b$12$6e2DSOJwq.Z/pz8LawWPH.WXj3mfkitZkS76ykL61NQy1cwOFYhCS', '$2b$12$6e2DSOJwq.Z/pz8LawWPH.',''),
(3, 'Ana Rodriguez','ARodriguez', 'arodriguez@email.com', '$2b$12$Sox8sFxljetZ41VEhcR2SOV8P2pD5dkyKjbFp0LZ6vzGLrb2kE/iu', '$2b$12$Sox8sFxljetZ41VEhcR2SO',''),
(4, 'Cristina Briones','CBriones', 'cbriones@email.com', '$2b$12$Sox8sFxljetZ41VEhcR2SOV8P2pD5dkyKjbFp0LZ6vzGLrb2kE/iu', '$2b$12$Sox8sFxljetZ41VEhcR2SO','')
(5, 'Jesus Lopez','JLopez', 'jlopez@email.com', '$2b$12$gIcSbXQrWqMHTFhbcNOguOQhSNDDq.nQpuX25Fgfy4HKrrIScnaWm', '$2b$12$gIcSbXQrWqMHTFhbcNOguO',''),
(6, 'Marivi Yepes','MYepes', 'myepes@email.com', '$2b$12$6e2DSOJwq.Z/pz8LawWPH.WXj3mfkitZkS76ykL61NQy1cwOFYhCS', '$2b$12$6e2DSOJwq.Z/pz8LawWPH.','')
;

INSERT INTO "group"
(id_group, name_group,id_owner)
VALUES
(1, 'Group Sprint 16',1),
(2, 'Group Sprint 17',2),
(3, 'Group lunch',3),
(4, 'Group Team Leaders',3)
;


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
(1, 'Rating participation 100%', 1, 'RatingTopic'  , '2023-04-20 00:00:00.000000', '2023-05-20 00:00:00.000000', False, 100,'9999-12-31 00:00:00.000000'),
(2, 'Rating No esta en el grupo', 1, 'RatingTopic' , '2023-04-18 00:00:00.000000', '2023-05-20 00:00:00.000000', True, 0,'9999-12-31 00:00:00.000000'),
(3, 'Rating preparado para votar', 2, 'RatingTopic', '2023-04-01 00:00:00.000000', '2023-05-20 00:00:00.000000', True, 0,'9999-12-31 00:00:00.000000'),
(4, '¿Cuándo vamos a la Oficina?', 3, 'MultipleChoiceTextTopic', '2023-02-12 00:00:00.000000', '2023-05-20 00:00:00.000000', True, 0,'9999-12-31 00:00:00.000000'),
(5, 'Rating enddate has expired', 1, 'RatingTopic', '2023-05-17 00:00:00.000000', '2023-05-19 00:00:00.000000', True, 50,'9999-12-31 00:00:00.000000'),
(6, 'Prueba topic multiple text', 1, 'MultipleChoiceTextTopic', '2023-05-17 00:00:00.000000', '9999-12-31 00:00:00.000000', True, 0,'9999-12-31 00:00:00.000000'),
(7, 'Rating permite reopen', 1, 'RatingTopic'     , '2023-05-17 00:00:00.000000', '9999-12-31 00:00:00.000000', False, 0,'9999-12-31 00:00:00.000000'),
(8, 'Rating Ya has contestdo', 2, 'RatingTopic'   , '2023-05-19 00:00:00.000000', '2023-06-30 00:00:00.000000', True, 50,'9999-12-31 00:00:00.000000')
;



-- 1 = completed, 0 = not completed
INSERT INTO topic_ticket
(user_id, topic_id, completed)
VALUES	  
(2, 1, 1),
(2, 2, 0),
(3, 2, 0),
(1, 3, 0),
(2, 3, 0),
(2, 4, 0),
(3, 4, 0),
(1, 5, 0),
(2, 5, 1),
(1, 6, 0),
(2, 6, 0),
(3, 6, 0),
(1, 7, 0),
(2, 7, 0),
(1, 8, 1),
(2, 8, 0)
;



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
(10, 4, 4, 'Me da igual'),
(11, 5, 1, 'Lunes, Miercoles'),
(12, 5, 2, 'Martes, Jueves'),
(13, 5, 3, 'Una semana lu, mi, otra ma, jue'),
(14, 5, 4, 'Me da igual'),
(15, 6, 1, 'Lunes, Miercoles'),
(16, 6, 2, 'Miércoles, Jueves'),
(17, 6, 3, 'Días alternos'),
(18, 6, 4, 'Me da igual')
;

INSERT INTO topic_answer
(id_topic_answer, id_topic, answer)
VALUES
(2, 1, 3),
(3, 5, 1),
(4, 8, 5)
;


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


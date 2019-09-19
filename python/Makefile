NAME=python

run:
	docker-compose build
	docker-compose up -d

stop:
	# docker stop ${NAME}_static_1 ${NAME}_app_1 ${NAME}_db_1
	# docker rm ${NAME}_static_1 ${NAME}_app_1 ${NAME}_db_1
	docker-compose down

sql:
	docker exec -it python_db_1 bash
	mysql -u hidakkathon -phidakkathon
	use sugori_rendez_vous;
	select event_id, created_user_id from i_event where event_id = 1;
	select * from i_participate_event where event_id = 1;
	select * from i_participate_event where user_id = "aaliyah_leannon102";
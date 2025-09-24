FROM postgrest/postgrest:latest

# PostgREST 설정 파일 복사
COPY postgrest.conf /etc/postgrest.conf


EXPOSE 3000

# PostgREST 실행
CMD ["postgrest", "/etc/postgrest.conf"]

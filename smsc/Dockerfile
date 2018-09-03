FROM java:8
LABEL maintainer "Pavlov Viktor <zogxray@gmail.com>"
EXPOSE 88 2775 3000

WORKDIR /app
COPY . ./

RUN chmod +x startsmppsim.sh
CMD ./startsmppsim.sh
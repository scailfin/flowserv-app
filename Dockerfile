FROM heikomueller/pie:0.1.2.flowserv

# Expose port for streamlit
EXPOSE 8501

COPY flowapp /app/flowapp
COPY README.rst /app/README.rst
COPY setup.py /app/setup.py
WORKDIR /app
RUN pip install /app
RUN rm -Rf /app/README.rst
RUN rm -Rf /app/setup.py

WORKDIR /

ARG FLOWSERV_API_DIR=/app/.flowserv
ARG FLOWSERV_BACKEND_CLASS=SerialWorkflowEngine
ARG FLOWSERV_BACKEND_MODULE=flowserv.controller.serial.engine
ARG FLOWSERV_DATABASE=sqlite:////app/db.sqlite

RUN flowserv init -f
RUN flowapp install helloworld
RUN flowapp install piesingle

ENV FLOWSERV_API_DIR=/app/.flowserv
ENV FLOWSERV_BACKEND_CLASS=SerialWorkflowEngine
ENV FLOWSERV_BACKEND_MODULE=flowserv.controller.serial.engine
ENV FLOWSERV_DATABASE=sqlite:////app/db.sqlite

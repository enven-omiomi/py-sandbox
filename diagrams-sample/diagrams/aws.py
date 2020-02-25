from diagrams import Diagram, Cluster
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb

with Diagram("api"):

    with Cluster("lambda"):
        lambdas = []
        for i in range(5):
            lambdas.append(Lambda("lambda"))

    APIGateway("agw") >> lambdas >> Dynamodb("db")

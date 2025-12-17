from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.programming.language import Python, Javascript
from diagrams.custom import Custom
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Flink
from diagrams.onprem.compute import Server
from diagrams.saas.chat import Slack # Using as generic chat/agent icon if needed or just generic
from diagrams.onprem.database import Postgresql # Placeholder for DBs
from diagrams.generic.device import Mobile, Tablet
from diagrams.gcp.ml import AdvancedSolutionsLab as BrainIcon # Alternate for "Brain"

# Since we don't have exact "Brain" or "React" in standard imports without specific providers, 
# we'll use closely matching available icons or generic ones.
# React: Javascript
# FastAPI: Python
# Agent: BrainIcon or generic

with Diagram("CapitalConnect Architecture", show=False, filename="capital_connect_architecture", outformat="png"):
    
    with Cluster("Client Side"):
        user = Mobile("User")
        frontend = Javascript("Frontend (React)")

    with Cluster("Backend Services"):
        backend = Python("Backend (FastAPI)")
        
        with Cluster("Orchestration"):
            agent = BrainIcon("Master Agent")
            
        with Cluster("Streaming"):
            kafka = Kafka("Apache Kafka")
            flink = Flink("Apache Flink")
    
    with Cluster("External/Mock Services"):
        credit_bureau = Server("Credit Bureau")
        crm = Server("CRM")

    # Flow
    user >> frontend >> backend
    backend >> agent
    backend >> kafka >> flink
    flink >> credit_bureau
    flink >> crm
    
    # PDF Generation part of Backend
    # Implied in backend logic

# libs/service_manager.py
from typing import Dict
from openai import AsyncOpenAI
from libs.services.essay_advisor.service import EssayAdvisorService
from libs.services.k9_helper.service import K9HelperService
from libs.services.base_service import BaseAssistantService

class AssistantServiceManager:
    _instance = None
    
    def __init__(self, client: AsyncOpenAI):
        self.client = client
        self.services: Dict[str, BaseAssistantService] = {}
        
    @classmethod
    def get_instance(cls) -> 'AssistantServiceManager':
        if cls._instance is None:
            raise RuntimeError("ServiceManager not initialized")
        return cls._instance
    
    @classmethod
    def initialize(cls, client: AsyncOpenAI) -> 'AssistantServiceManager':
        if cls._instance is None:
            cls._instance = cls(client)
        return cls._instance
    
    def initialize_services(self, config: dict):
        """
        初始化所有助手服務
        """
        self.services = {
            "essay_advisor": EssayAdvisorService(
                client=self.client,
                assistant_id=config.get("ESSAY_ADVISOR_ID")
            ),
            "k9_helper": K9HelperService(
                client=self.client,
                assistant_id=config.get("K9_HELPER_ID")
            )
        }
    
    def get_service(self, service_name: str) -> BaseAssistantService:
        return self.services.get(service_name)

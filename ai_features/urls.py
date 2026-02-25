from django.urls import path
from .views import SimplifyView, StructureView, ExplainWordView, AgentOptimizeReadingView

urlpatterns = [
    # POST {"text": "..."} → {"simplified": "..."}
    path("simplify/", SimplifyView.as_view(), name="ai-simplify"),

    # POST {"text": "..."} → {"structured": "..."}
    path("structure/", StructureView.as_view(), name="ai-structure"),

    # POST {"word": "...", "context": "..."} → {"word": "...", "explanation": "..."}
    path("explain/", ExplainWordView.as_view(), name="ai-explain"),

    # POST {"file_id": int, "text": "...", "current_settings": {...}} 
    path("agent/optimize-reading/", AgentOptimizeReadingView.as_view(), name="agent-optimize-reading"),
]

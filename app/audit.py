from datetime import datetime
import uuid

class AuditLogger:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())[:8] 
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.steps = []

    def log(self, step_name: str, status: str, detail: str, data: dict = None):
        """
        Registra um passo do processo.
        :param step_name: Nome da etapa (ex: "OCR", "Policy Parser")
        :param status: "SUCCESS", "WARNING", "FAILURE", "INFO"
        :param detail: Descrição humana do que aconteceu
        :param data: (Opcional) Dicionário com dados técnicos para debug
        """
        entry = {
            "step": step_name,
            "status": status,
            "detail": detail,
            "data": data, 
            "time": datetime.now().strftime("%H:%M:%S")
        }
        self.steps.append(entry)

    def get_summary(self):
        return {
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "steps": self.steps
        }
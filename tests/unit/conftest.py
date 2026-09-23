import sys
import warnings
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "src" / "query_service"
sys.path.insert(0, str(SRC))

# O TestClient de Starlette usa o atajo `app` de httpx, que está
# deprecado em versões novas de httpx. O warning é interno da
# librería e não afeta o comportamento; o silenciamos para CI limpo.
warnings.filterwarnings(
    "ignore",
    message=r"The 'app' shortcut is now deprecated.*",
    category=DeprecationWarning,
)


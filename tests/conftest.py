import os
import sys
import types

os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017")
os.environ.setdefault("PIPER_EXE", "piper.exe")
os.environ.setdefault("PIPER_VOICE", "voice.onnx")

# Stub sentence_transformers so tests never load the real embedding model
# (avoids a multi-hundred-MB download / GPU dependency just to run unit tests).
if "sentence_transformers" not in sys.modules:
    stub = types.ModuleType("sentence_transformers")

    class _StubSentenceTransformer:
        def __init__(self, *args, **kwargs):
            pass

        def encode(self, text):
            import numpy as np

            return np.array([float(len(text))] * 4)

    stub.SentenceTransformer = _StubSentenceTransformer
    sys.modules["sentence_transformers"] = stub

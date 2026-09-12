# Vision Data Auditor

Audits a JSON image manifest for missing files, byte-identical duplicates, class counts, and a simple class-imbalance ratio—without requiring PyTorch, TensorFlow, or Pillow.

## Manifest

```json
[{"path":"images/cat-001.jpg","label":"cat"},{"path":"images/dog-001.jpg","label":"dog"}]
```

## Usage

```bash
python -m unittest discover -s tests -v
python -m pip install .
vision-data-auditor manifest.json --root dataset
```

Duplicate detection uses SHA-256 of raw files, not perceptual similarity. The tool does not inspect annotation quality or image semantics.

## License

MIT.

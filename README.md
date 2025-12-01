# RNA MAP Mini

RNA MAP: Rapid analysis of RNA mutational profiling (MaP) experiments.

A Python package for analyzing DMS-MaPseq sequencing data to identify RNA structural information through mutation analysis.

## Features

- Quality control and read alignment processing
- Bit vector generation (Python and C++ implementations)
- Mutation pattern analysis and visualization
- Support for paired-end and single-end reads
- C++ extensions for improved performance

## Installation

### From Source

```bash
git clone https://github.com/jyesselm/rna-map-mini.git
cd rna-map-mini
pip install .
```

### With C++ Extensions

The C++ extensions will be automatically compiled during installation if:
- A C++17 compatible compiler is available
- pybind11 is installed

To install with optional dependencies:

```bash
# With pysam support
pip install .[pysam]

# With optuna support
pip install .[optuna]

# Development dependencies
pip install .[dev]
```

## Quick Start

```python
from pathlib import Path
from rna_map_mini.pipeline import generate_bit_vectors
from rna_map_mini.core.config import BitVectorConfig

config = BitVectorConfig(
    qscore_cutoff=25,
    num_of_surbases=10,
    map_score_cutoff=15,
)

result = generate_bit_vectors(
    sam_path=Path("aligned.sam"),
    fasta=Path("reference.fasta"),
    output_dir=Path("output"),
    config=config,
    paired=False
)
```

## Parameter Tuning

For comprehensive documentation on all tunable parameters and suggested new parameters for customization, see [PARAMETERS.md](PARAMETERS.md).

The package supports extensive parameter customization for:
- Quality score filtering
- Mapping quality thresholds
- Mutation detection constraints
- Output format and storage
- Performance optimization

See the parameters documentation for detailed information on existing parameters and suggestions for future enhancements.

## Package Structure

- `rna_map_mini.io`: Input/output operations (FASTA, FASTQ, SAM, CSV parsing)
- `rna_map_mini.core`: Core data structures (AlignedRead, BitVector, Config)
- `rna_map_mini.pipeline`: Pipeline orchestration (BitVectorGenerator)
- `rna_map_mini.analysis`: Mutation analysis (MutationHistogram, statistics)
- `rna_map_mini.visualization`: Plotting and visualization

## Requirements

- Python >= 3.10
- numpy >= 1.21
- pandas >= 1.5
- pyyaml >= 6.0
- tabulate >= 0.9
- matplotlib >= 3.5
- pybind11 >= 2.10 (for C++ extensions)

## Development

```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/

# Run linting
ruff check .
black --check .
```

## C++ Extensions

The package includes C++ extensions for improved performance. The C++ module is automatically built during installation using pybind11.

To build manually:

```bash
cd cpp
./build.sh
```

## License

MIT License

## Author

Joe Yesselman (jyesselm@unl.edu)


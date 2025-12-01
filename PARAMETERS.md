# Tunable Parameters for RNA MAP Mini

This document lists all existing tunable parameters and suggests new parameters for enhanced customization and parameter tuning.

## Existing Tunable Parameters

### 1. Mapping Configuration (`MappingConfig`)

Located in: `rna_map_mini/core/config.py`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip_fastqc` | bool | `False` | Skip FastQC quality control step |
| `skip_trim_galore` | bool | `False` | Skip Trim Galore adapter trimming step |
| `tg_q_cutoff` | int | `20` | Trim Galore quality score cutoff (Phred score) |
| `bt2_alignment_args` | str | `"--local;--no-unal;--no-discordant;--no-mixed;-X 1000;-L 12;-p 16"` | Bowtie2 alignment arguments (semicolon-separated) |
| `save_unaligned` | bool | `False` | Save unaligned reads to file |

**Usage:**
```python
from rna_map_mini.core.config import MappingConfig

config = MappingConfig(
    tg_q_cutoff=25,
    bt2_alignment_args="--local;--no-unal;-X 2000"
)
```

### 2. Bit Vector Configuration (`BitVectorConfig`)

Located in: `rna_map_mini/core/config.py`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `qscore_cutoff` | int | `25` | Quality score cutoff for read nucleotides (Phred score) |
| `num_of_surbases` | int | `10` | Number of surrounding bases for ambiguity check in deletions |
| `map_score_cutoff` | int | `15` | Minimum mapping quality score cutoff |
| `plot_sequence` | bool | `False` | Whether to plot sequence/structure on plots |
| `summary_output_only` | bool | `False` | Only generate summary files (skip bit vector files) |
| `storage_format` | StorageFormat | `TEXT` | Storage format for bit vectors (`TEXT` or `JSON`) |
| `use_cpp` | bool | `False` | Whether to use C++ implementation (if available) |
| `use_pysam` | bool | `False` | Whether to use pysam for SAM parsing (faster, more robust) |
| `stricter_constraints` | StricterConstraints \| None | `None` | Optional stricter constraints (see below) |

**Usage:**
```python
from rna_map_mini.core.config import BitVectorConfig

config = BitVectorConfig(
    qscore_cutoff=30,
    num_of_surbases=15,
    map_score_cutoff=20,
    use_cpp=True
)
```

### 3. Stricter Constraints (`StricterConstraints`)

Located in: `rna_map_mini/core/config.py`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_mut_distance` | int | `5` | Minimum distance between mutations (in nucleotides) |
| `percent_length_cutoff` | float | `0.10` | Minimum percent of reference length required (0.0-1.0) |
| `mutation_count_cutoff` | int | `5` | Maximum number of mutations allowed per read |

**Usage:**
```python
from rna_map_mini.core.config import BitVectorConfig, StricterConstraints

stricter = StricterConstraints(
    min_mut_distance=10,
    percent_length_cutoff=0.20,
    mutation_count_cutoff=10
)

config = BitVectorConfig(
    stricter_constraints=stricter
)
```

### 4. Global Parameters (from `default.yml`)

Located in: `rna_map_mini/resources/default.yml`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `overwrite` | bool | `False` | Overwrite existing output files |
| `restore_org_behavior` | bool | `False` | Restore original behavior (legacy mode) |
| `stricter_bv_constraints` | bool | `False` | Enable stricter bit vector constraints |

## Suggested New Parameters

### A. Quality Control Parameters

#### 1. **Read Length Filters**
- `min_read_length` (int, default: `0`): Minimum read length to process
- `max_read_length` (int, default: `None`): Maximum read length to process
- `min_aligned_length` (int, default: `0`): Minimum aligned length required
- `min_alignment_fraction` (float, default: `0.0`): Minimum fraction of read that must align

**Rationale**: Filter out very short or very long reads that may be artifacts or chimeras.

#### 2. **Quality Score Parameters**
- `min_mean_qscore` (float, default: `0.0`): Minimum mean quality score across read
- `qscore_window_size` (int, default: `None`): Window size for sliding window quality filtering
- `qscore_window_threshold` (float, default: `None`): Quality threshold for sliding window
- `qscore_trim_ends` (bool, default: `False`): Trim low-quality bases from read ends

**Rationale**: More sophisticated quality filtering beyond single-position cutoff.

### B. Alignment Parameters

#### 3. **CIGAR Operation Handling**
- `max_deletion_length` (int, default: `None`): Maximum deletion length to process
- `max_insertion_length` (int, default: `None`): Maximum insertion length to process
- `max_soft_clip_length` (int, default: `None`): Maximum soft clip length to tolerate
- `process_hard_clips` (bool, default: `False`): Whether to process hard-clipped bases
- `min_match_length` (int, default: `0`): Minimum match length required

**Rationale**: Control how different CIGAR operations are handled, especially for noisy data.

#### 4. **Deletion Ambiguity Parameters**
- `deletion_ambiguity_window` (int, default: `num_of_surbases`): Window size for deletion ambiguity check
- `deletion_ambiguity_threshold` (float, default: `0.5`): Fraction of surrounding bases that must match for unambiguous deletion
- `require_unambiguous_deletions` (bool, default: `False`): Reject reads with ambiguous deletions

**Rationale**: Fine-tune deletion ambiguity detection, which is critical for DMS-MaPseq.

### C. Mutation Detection Parameters

#### 5. **Mutation Filtering**
- `min_mutation_confidence` (float, default: `0.0`): Minimum confidence score for mutation calls
- `mutation_type_weights` (dict, default: `None`): Weights for different mutation types (A, C, G, T)
- `exclude_mutations_near_ends` (bool, default: `False`): Exclude mutations near read ends
- `end_exclusion_length` (int, default: `5`): Number of bases to exclude from each end

**Rationale**: Filter mutations based on confidence and position.

#### 6. **Paired-End Read Parameters**
- `require_both_ends` (bool, default: `False`): Require both reads in pair to pass filters
- `merge_strategy` (str, default: `"union"`): How to merge paired reads (`"union"`, `"intersection"`, `"consensus"`)
- `max_pair_distance` (int, default: `None`): Maximum expected distance between paired reads
- `min_pair_overlap` (int, default: `0`): Minimum overlap required between paired reads

**Rationale**: Control how paired-end reads are merged and processed.

### D. Output and Storage Parameters

#### 7. **Output Control**
- `output_compression` (str, default: `None`): Compression format (`"gzip"`, `"bz2"`, `None`)
- `max_bit_vectors_per_file` (int, default: `None`): Maximum bit vectors per output file
- `split_by_reference` (bool, default: `True`): Split output files by reference sequence
- `include_rejected_reads` (bool, default: `False`): Include rejected reads in output
- `rejection_reason_detail` (bool, default: `False`): Include detailed rejection reasons

**Rationale**: Control output format and organization for large datasets.

#### 8. **Summary Statistics Parameters**
- `mutation_bin_size` (int, default: `1`): Bin size for mutation count histograms
- `coverage_bin_size` (int, default: `1`): Bin size for coverage histograms
- `calculate_percentiles` (bool, default: `False`): Calculate percentile statistics
- `percentiles` (list, default: `[25, 50, 75, 90, 95, 99]`): Percentiles to calculate

**Rationale**: Customize summary statistics for different analysis needs.

### E. Performance Parameters

#### 9. **Processing Optimization**
- `chunk_size` (int, default: `None`): Number of reads to process in each chunk
- `max_workers` (int, default: `1`): Maximum number of parallel workers
- `memory_limit` (int, default: `None`): Memory limit in MB
- `progress_update_interval` (int, default: `1000`): Number of reads between progress updates

**Rationale**: Optimize performance for large datasets and resource-constrained environments.

#### 10. **C++ Implementation Parameters**
- `cpp_optimization_level` (str, default: `"O3"`): C++ compiler optimization level
- `cpp_parallel_threads` (int, default: `None`): Number of threads for C++ parallel processing
- `cpp_memory_pool_size` (int, default: `None`): Memory pool size for C++ implementation

**Rationale**: Fine-tune C++ implementation performance.

### F. Advanced Filtering Parameters

#### 11. **Read Filtering**
- `min_coverage_depth` (int, default: `0`): Minimum coverage depth required at position
- `max_coverage_depth` (int, default: `None`): Maximum coverage depth (for outlier removal)
- `coverage_smoothing_window` (int, default: `None`): Window size for coverage smoothing
- `exclude_low_complexity` (bool, default: `False`): Exclude low-complexity regions
- `low_complexity_threshold` (float, default: `0.5`): Threshold for low-complexity detection

**Rationale**: Advanced filtering for high-quality mutation detection.

#### 12. **Reference Sequence Parameters**
- `min_reference_length` (int, default: `0`): Minimum reference sequence length
- `max_reference_length` (int, default: `None`): Maximum reference sequence length
- `exclude_reference_patterns` (list, default: `[]`): Regex patterns for reference sequences to exclude
- `reference_name_filter` (str, default: `None`): Filter reference sequences by name pattern

**Rationale**: Control which reference sequences are processed.

### G. Visualization Parameters

#### 13. **Plot Customization**
- `plot_dpi` (int, default: `300`): Resolution for output plots
- `plot_format` (str, default: `"png"`): Output format (`"png"`, `"pdf"`, `"svg"`)
- `plot_width` (int, default: `10`): Plot width in inches
- `plot_height` (int, default: `6`): Plot height in inches
- `plot_style` (str, default: `"default"`): Matplotlib style (`"default"`, `"seaborn"`, etc.)
- `plot_color_scheme` (str, default: `"default"`): Color scheme for plots

**Rationale**: Customize visualization output for publications and presentations.

## Implementation Priority

### High Priority (Most Impactful)
1. **Read Length Filters** - Essential for quality control
2. **Deletion Ambiguity Parameters** - Critical for DMS-MaPseq accuracy
3. **Paired-End Read Parameters** - Important for paired-end data
4. **Mutation Filtering** - Improves mutation detection quality

### Medium Priority (Useful Enhancements)
5. **CIGAR Operation Handling** - Better control over alignment processing
6. **Output Control** - Important for large datasets
7. **Summary Statistics Parameters** - Enhanced analysis capabilities
8. **Performance Parameters** - Better scalability

### Low Priority (Nice to Have)
9. **Quality Score Parameters** - More sophisticated filtering
10. **Advanced Filtering Parameters** - Specialized use cases
11. **Visualization Parameters** - Output customization
12. **C++ Implementation Parameters** - Performance fine-tuning

## Example Configuration

Here's an example of how a comprehensive configuration might look:

```python
from rna_map_mini.core.config import BitVectorConfig, StricterConstraints

# Comprehensive configuration example
config = BitVectorConfig(
    # Existing parameters
    qscore_cutoff=30,
    num_of_surbases=15,
    map_score_cutoff=20,
    use_cpp=True,
    
    # Suggested new parameters (when implemented)
    # min_read_length=50,
    # max_read_length=200,
    # min_aligned_length=40,
    # min_alignment_fraction=0.8,
    # max_deletion_length=10,
    # deletion_ambiguity_window=15,
    # require_unambiguous_deletions=True,
    # exclude_mutations_near_ends=True,
    # end_exclusion_length=5,
    # merge_strategy="consensus",
    # output_compression="gzip",
    # chunk_size=10000,
    # max_workers=4,
    
    stricter_constraints=StricterConstraints(
        min_mut_distance=10,
        percent_length_cutoff=0.20,
        mutation_count_cutoff=10
    )
)
```

## Notes

- All suggested parameters should maintain backward compatibility with default values
- Parameters should be validated with appropriate ranges/types
- Consider adding parameter validation and helpful error messages
- Document parameter interactions (e.g., `qscore_cutoff` vs `min_mean_qscore`)
- Consider parameter presets for common use cases (e.g., "high_sensitivity", "high_specificity", "fast")


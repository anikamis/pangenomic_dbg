# pangenomic_dbg

## data collection:

example: mycoplasm genitalium (taxid: 2097)

1. search on propan (https://ngdc.cncb.ac.cn/propan/search)

2. navigate to “Analysed Strain Information”

3. see strains listed by GenBank accession

4. for any number of strains, click on GenBank accession link to navigate to NCBI

5. download assemblies on NCBI (for simplicity purposes at the moment, only choose strains if the assembly file available for download is complete, e.g. there is only one fasta header under which the entire genome sequence is listed)

6. create a text file containing the locations of genome fastas (e.g. example_runs/strains.txt)

7. create a directory containing all genome fasta files (e.g. example_runs/genomes)

## run process:

**usage:** python3 pangenome.py -i `<input file>` -o `<output file>` -k `<kmer_size>` [-u] [-q `<query>`]

**-i:** input text file containing location of genome fasta file for each strain, separated by newlines

**-o:** desired prefix for json output file of graph

**-k:** kmer size

**-u:** flag to generate uncompressed pangenome graph (default is compressed) [optional]

**-q:** name of either a strain or "core", queries graph and outputs fasta file of unique sequences named `<query>`.fasta [optional]

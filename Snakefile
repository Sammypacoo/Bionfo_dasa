# Dasa/Snakefile

# Defina as variáveis do caminho
annovar_path = "Dasa/annovar"
input_vcf = "Dasa/vcf/NIST.vcf"
#output_dir = "Dasa/"

# # Regra principal
rule all:
     input:
        "Dasa/annotated_variants.hg19_multianno.csv"
    

 # Regra para baixar avsnp151
rule download_dbsnp:
     output:
         "Dasa/annovar/humandb/hg19_avsnp151.txt",
         "Dasa/annovar/humandb/hg19_avsnp151.txt.idx"
     shell:
         """
         perl {annovar_path}/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar avsnp151 {annovar_path}/humandb/
         """
 # Regra para baixar gnomAD
rule download_gnomad:
     output:
         "Dasa/annovar/humandb/hg19_gnomad211_genome.txt",
         "Dasa/annovar/humandb/hg19_gnomad211_genome.idx"
     shell:
         """
         perl {annovar_path}/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar gnomad211_genome {annovar_path}/humandb/
         """
 # Regra para baixar refGene
rule download_refgene:
     output:
         "Dasa/annovar/humandb/hg19_refGene.txt"
     shell:
         """
         perl {annovar_path}/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar refGene {annovar_path}/humandb/
         """

# Regra para converter VCF para ANNOVAR
rule convert_vcf_to_annovar:
    input:
        vcf=input_vcf
    output:
        "Dasa/variants.avinput"
    shell:
        """
        perl {annovar_path}/convert2annovar.pl -format vcf4 {input.vcf} > {output}
        """

# Regra para anotar variantes
rule annotate_variants:
    input:
        avinput="Dasa/variants.avinput",
        dbsnp="Dasa/annovar/humandb/hg19_avsnp151.txt",
        gnomad="Dasa/annovar/humandb/hg19_gnomad211_genome.txt",
        refgene="Dasa/annovar/humandb/hg19_refGene.txt"
    output:
        "Dasa/annotated_variants.hg19_multianno.csv"
    params:
        db="refGene,avsnp151,gnomad211_genome"
        #db="refGene,avsnp151"

    shell:
        """
        perl {annovar_path}/table_annovar.pl {input.avinput} {annovar_path}/humandb/ \
        -buildver hg19 -out Dasa/annotated_variants -protocol {params.db} -operation g,f,f \
        -nastring . -csvout --otherinfo
        """

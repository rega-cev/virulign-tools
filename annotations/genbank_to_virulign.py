from xml.etree.ElementTree import ElementTree
import sys

if len(sys.argv) < 4:
    print "Usage: python genbank_to_virulign.py genbank_insdseq.xml orf-name seq-start seq-end"
    sys.exit()

#get the genbank entry in the INSDSEQ XML format
xml_file = sys.argv[1]
orf_name = sys.argv[2]
#1-based ORF start and stop position
ref_seq_start = int(sys.argv[3])
ref_seq_end = int(sys.argv[4])

doc = ElementTree(file=xml_file)

#orf sequence
sequence_prefix = '/INSDSeq_sequence' 
sequence = doc.find('.' + sequence_prefix).text
class Region:
    def __init__(self, start=None, end=None, name=None):
        self.start = start 
        self.end = end
        self.name = name 

regions = []

#find all features
feature_table_prefix = '/INSDSeq_feature-table/INSDFeature'
for e in doc.findall('.' + feature_table_prefix):
    #select the features we're interested in
    if e.find('INSDFeature_key').text == 'mat_peptide':
        interval_prefix = '/INSDFeature_intervals/INSDInterval/'
       
        start = int(e.find('.' + interval_prefix + 'INSDInterval_from').text)
        end = int(e.find('.' + interval_prefix + 'INSDInterval_to').text)
        region_name = ''

        qualifier_prefix = '/INSDFeature_quals/INSDQualifier'
        for q in e.findall('.' + qualifier_prefix):
            if q.find('INSDQualifier_name').text == 'product':
                region_name = q.find('INSDQualifier_value').text

        regions.append(Region(start, end, region_name))

#1-based ref_seq_start and ref_seq_end, therefore -1
#(note the extra -1 for the end of the range)
orf_sequence = sequence[(ref_seq_start-1):(ref_seq_end-1)-1]

#XML UTF8 header
print '<?xml version="1.0" encoding="UTF-8"?>'

print '<orf name=\"' + orf_name + '\" ' + \
            'referenceSequence=\"' + orf_sequence + '\" >'

for region in regions:
    #e.g.: the CDS of NC_002031 starts at position 119 (https://www.ncbi.nlm.nih.gov/nucleotide/NC_002031)
    #Since the first protein starts with the CDS, its start position is as well 119.
    #Thus: region.start - ref_seq_start = 119 - 119 = 0.
    #The virulign XML format is 1-based: therefore (region.start - ref_seq_start) + 1.
    #The same idea holds for the end position, with an important remark (see below ***).
    start = (region.start - ref_seq_start) + 1
    end = region.end - ref_seq_start + 1
    #***HOWEVER:
    #The virulign format accepts a start position UNTILL the end: thus an additional +1 is necessary
    end = end + 1
    print "\t<protein abbreviation=\"" + region.name + "\" startPosition=\"" + \
        str(start) + "\" stopPosition=\"" + str(end) + "\" />"

print '</orf>'

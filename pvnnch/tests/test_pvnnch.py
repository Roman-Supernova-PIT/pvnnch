from pvnnch import nn2vec

### Tests I want:
### Test regular LC with full S-T and S-S from the pipeline
### Test LC with only S-T from pipeline
### Test LC with full S-T and partial S-S from pipeline
### Input one LC and get the input back out 

def test_SS_ST(full_SS_ST_data):
    print(nn2vec(*full_SS_ST_data))
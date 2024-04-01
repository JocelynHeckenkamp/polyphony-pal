import music_analysis.music_xml_parser as mxp
import music_analysis.error as e
import music_analysis.rule27 as r27
import music_analysis.rules1to13 as r113
import music_analysis.rules14to26 as r1426
import music_analysis.rules25_28_31 as r2531

fn = "../music-xml-examples/rule25.musicxml"

if __name__ == '__main__':
    sw = mxp.getScoreWrapper(fn)
    #print(sw)
    
    #for c in sw.chord_wrappers:
        #print(c.location, c.chord_obj.fullName)
        #print(c.melodic_intervals)

    # chords iterated through by next pointer
    curr = sw.chord_wrappers[0]
    errors = r27.check_rule_27(sw)
    while(curr is not None):
        #print(curr, curr.inversion)
        errors.extend(r1426.check_rules_14_to_26(curr, sw))
        errors.extend(r113.check_rules_1_to_13(curr, sw))
        errors.extend(r2531.check_rules_25_28to31(curr, sw))
        curr = curr.next

    for error in errors:
        print(error)
        
    # sw.score.show()
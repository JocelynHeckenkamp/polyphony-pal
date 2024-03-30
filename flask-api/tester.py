import music_analysis.music_xml_parser as mxp
import music_analysis.error as e
import music_analysis.rule27 as r27
import music_analysis.rules1to13 as r113
import music_analysis.rules14to26 as r1426

fn = "../music-xml-examples/voice-leading-1.musicxml"

if __name__ == '__main__':
    sw = mxp.getScoreWrapper(fn)
    #print(sw)
    
    #for c in sw.chord_wrappers:
        #print(c.location, c.chord_obj.fullName)
        #print(c.melodic_intervals)

    # chords iterated through by next pointer
    curr = sw.chord_wrappers[0]
    print(r27.check_rule_27(sw))
    while(curr is not None):
        print(curr, curr.inversion)
        errors = r1426.check_rules_14_to_26(curr, sw)
        errors.extend(r113.check_rules_1_to_13(curr, sw))
        for error in errors:
            print(error)
        curr = curr.next

        
    # sw.score.show()
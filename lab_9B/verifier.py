import traceback
import pprint

def validate_rendering(blobs):
    return all("pos" in b and "identifier" in b and "texture" in b and "player" in b for b in blobs)

def sanitize_rendering(rendered):
    rendered.pop("identifier")

def frame2set(frame):
    return {(("pos", tuple(blob["pos"])), ("texture", blob["texture"]), ("player", blob["player"])) for blob in frame}

def sort_blob_set(blobs):
    return [dict(b) for b in sorted(blobs)]

def verify_replay(student_trace, reference_trace):
    assert len(student_trace) == len(reference_trace)
    # pprint.pprint(zip(student_trace, reference_trace))
    for fid, (student, reference) in enumerate(zip(student_trace, reference_trace)):
        stustatus, stuframe = student
        refstatus, refframe = reference
        if not validate_rendering(stuframe):
            return "Invalid frame (contains a malformed blob): {}".format(pprint.pformat(stuframe))
        stuset, refset = frame2set(stuframe), frame2set(refframe)
        if stuset != refset or stustatus != refstatus:
            lines = ["", "# Frame #{} diverges from reference.".format(fid)]
            extraneous, missing = stuset - refset, refset - stuset
            if stustatus != refstatus:
                lines.append("\n## Incorrect game status: {} (expected {})".format(stustatus, refstatus))
            if missing:
                lines.append("\n## Missing from your rendering:")
                lines.append(pprint.pformat(sort_blob_set(missing)))
            if extraneous:
                lines.append("\n## Found in your rendering, but unexpected:")
                lines.append(pprint.pformat(sort_blob_set(extraneous)))
            return "\n".join(lines)

TRANSLATIONVECTOR_TEMPLATE = "Unexpected result: expected translation vector {}, got {}, for rectangles {}, {}."
INTERSECTION_TEMPLATE = "Unexpected result: your implementation claims that {} {} {}."

def verify_intersection(result, reference):
    for (r1, r2, res), ref in zip(result, reference):
        if res != ref:
            verb = "intersects" if res else "does not intersect"
            return INTERSECTION_TEMPLATE.format(r1, verb, r2)

def verify_translationvector(result, reference):
    for (r1, r2, res), ref in zip(result, reference):
        if res != ref:
            return TRANSLATIONVECTOR_TEMPLATE.format(ref, res, r1, r2)

def verify(result, input_data, gold):
    restype, result = result

    if restype == "error":
        return False, "raised an error: {}".format(result)

    try:
        test_type = input_data.pop("type")
        verifn = {"replay": verify_replay,
                  "intersection": verify_intersection,
                  "translationvector": verify_translationvector}[test_type]
        errmsg = verifn(result, gold)

        if errmsg is not None:
            return False, errmsg
        else:
            return True, "is correct. Hooray!"
    except:
        traceback.print_exc()
        return False, "crashed :(. Stack trace is printed above so you can debug."

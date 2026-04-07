import random

def generate_timetable_data(classes, subjects):
    """
    Generates a conflict-free timetable utilizing a simple greedy approach.
    Assumes 5 days a week, 6 slots a day.
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods = 6
    
    # Track teacher occupation: teacher_tracker[teacher_id][day][slot] = Boolean
    teacher_tracker = {}
    
    timetable = {} # format: {class_id: {day: [subject_or_free, ... ] }}
    
    for cls in classes:
        cid = str(cls['_id'])
        timetable[cid] = {day: ["Free"] * periods for day in days}
        
        # Get subjects for this class
        class_subs = [s for s in subjects if s['class_id'] == cid]
        
        # Create a pool of hours to distribute
        pool = []
        for s in class_subs:
            pool.extend([s] * s['weekly_hours'])
            
        # Shuffle pool for some randomness
        random.shuffle(pool)
        
        # Distribute greedy
        for day in days:
            for slot in range(periods):
                if not pool:
                    break
                
                # Pick a valid subject from pool
                assigned = False
                for i, sub in enumerate(pool):
                    tid = sub['teacher_id']
                    
                    if tid not in teacher_tracker:
                        teacher_tracker[tid] = {d: [False]*periods for d in days}
                        
                    # Rule 1: No teacher clash
                    if not teacher_tracker[tid][day][slot]:
                        # Assign
                        timetable[cid][day][slot] = sub
                        teacher_tracker[tid][day][slot] = True
                        pool.pop(i)
                        assigned = True
                        break
                        
                if not pool:
                    break
    
    return timetable

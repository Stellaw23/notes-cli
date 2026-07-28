import json
import datetime

def load_notes():
    try:
        with open("notes.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_notes(notes):
    with open("notes.json", "w") as w:
        return json.dump(notes, w)

def add_note(content, tag):
    notes = load_notes()
    if not notes:
        new_id = 1
    else:
        new_id = int(max(notes, key=lambda note: note["note_id"])["note_id"]) + 1
    new_note_dict = {"note_id": new_id, "content": content, "tag": tag, "created_at": datetime.datetime.now().isoformat(), "synced": False}
    notes.append(new_note_dict)
    return save_notes(notes)

def list_notes():
    notes = load_notes()
    for note in notes:
        id = note["note_id"]
        content = note["content"]
        tag = note["tag"]
        print(f"{id}: {content} #{tag}")

def search_notes(keyword=None, tag=None):
    notes = load_notes()
    results = []
    for note in notes:
        if tag is not None and note["tag"] != tag: 
            continue
        if keyword is not None and keyword not in note["content"]:
            continue
        else:
            results.append(note)
    return results

def delete_notes(id):
    notes = load_notes()
    results = [note for note in notes if note["note_id"] != id]
    return save_notes(results)

from roam import call_roam_api, get_today_uid

def sync_notes():
    notes = load_notes()
    for note in notes:
        if not note.get("synced", False): 
            note_for_roam = f"{note["content"]} #{note["tag"]}"
            call_roam_api("data.block.fromMarkdown", [
                {
                    "location": {"parent-uid": get_today_uid(), "order": "last"},
                    "markdown-string": note_for_roam,
                    }
            ])
            note["synced"] = True
        else:
            continue
    return save_notes(notes)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("content")
    add_parser.add_argument("--tag")

    list_parser = subparsers.add_parser("list")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--keyword")
    search_parser.add_argument("--tag")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    sync_parser = subparsers.add_parser("sync")


    args = parser.parse_args()

    if args.command == "add":
        add_note(args.content, args.tag)

    if args.command == "list":
        list_notes()

    if args.command == "search":
        for note in search_notes(args.keyword, args.tag):
            print(note)
        
    if args.command == "delete":
        delete_notes(args.id)

    if  args.command == "sync":
        sync_notes()


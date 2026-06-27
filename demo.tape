# VHS tape for the tool tuning demo gif (https://github.com/charmbracelet/vhs).
# Regenerate from the repo root with: vhs demo.tape
# It replays the committed sample output so the gif is deterministic.
Output demo.gif

Set FontSize 15
Set Width 1200
Set Height 720
Set Padding 18

Hide
Type "clear"
Enter
Show

Type "# Tune one tool contract: fail the vague contract, pass the sharper one"
Enter
Sleep 1000ms
Type "sed -n '1,80p' docs/tool_tuning_demo_sample.txt"
Enter
Sleep 4s

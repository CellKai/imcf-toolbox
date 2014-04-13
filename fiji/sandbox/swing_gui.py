from javax.swing import JPanel, JComboBox, JLabel, JFrame, JButton
from java.awt import GridLayout
from java.awt.event import ActionListener


class Listener(ActionListener):
  def __init__(self, label, cb):
    self.label = label
    self.cb = cb
  def actionPerformed(self, event):
    sel = self.cb.getSelectedItem()
    roimgr.select(roi_ni[sel])


class ButtonListener(ActionListener):
  def __init__(self, btn):
    self.btn = btn
  def actionPerformed(self, event):
    print event


def update_roi_mappings():
    global roi_in
    global roi_ni
    for i in range(roimgr.getCount()):
        name = roimgr.getName(i)
        roi_in.append(name)
        roi_ni[name] = i


roimgr = RoiManager.getInstance()
roi_ni = {}
roi_in = []
update_roi_mappings()
print roi_in
print roi_ni


choice_list = ["foo", "bar", "777"]

lbl1 = JLabel("foo label")
lbl2 = JLabel("bar label")

main_panel = JPanel()

### panel 1
panel1 = JPanel()
panel1.add(lbl1)
cb1 = JComboBox(choice_list)
btn1 = JButton("Accept")
btn1.addActionListener(ButtonListener(btn1))
panel1.add(cb1)
panel1.add(btn1)

### panel 2
panel2 = JPanel()
panel2.add(lbl2)
cb2 = JComboBox(sorted(list(roi_ni.keys())))
cb2.addActionListener(Listener(lbl2, cb2))
panel2.add(cb2)

frame = JFrame("Swing GUI Test Frame")
frame.getContentPane().add(main_panel)
main_panel.add(panel1)
main_panel.add(panel2)
frame.pack()
frame.setVisible(True)

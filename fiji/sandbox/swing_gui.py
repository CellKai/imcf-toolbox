from javax.swing import JPanel, JComboBox, JLabel, JFrame, JButton, JList
from java.awt import GridLayout
from java.awt.event import ActionListener

import javax.swing
from fiji.scripting import Weaver
import sys


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

wcode = Weaver.inline(
	"""
javax.swing.AbstractListModel m = new javax.swing.AbstractListModel() {
    String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
    public int getSize() { return strings.length; }
    public Object getElementAt(int i) { return strings[i]; }
};
return m;
        """, {}, javax.swing.AbstractListModel)
print "Weaver created!"
listmodel = wcode.call()
print "Weaver called!"

roimgr = RoiManager.getInstance()
if roimgr is None:
  print "No ROIs defined."
  sys.exit(0)
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
cb2 = JComboBox(sorted(roi_ni.keys()))
cb2.addActionListener(Listener(lbl2, cb2))
panel2.add(cb2)

### panel 3
pnl3 = JPanel()
lst1 = JList(listmodel)
pnl3.add(lst1)

frame = JFrame("Swing GUI Test Frame")
frame.getContentPane().add(main_panel)
main_panel.add(panel1)
main_panel.add(panel2)
main_panel.add(pnl3)
frame.pack()
frame.setVisible(True)

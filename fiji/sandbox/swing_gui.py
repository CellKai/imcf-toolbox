from javax.swing import JScrollPane, JPanel, JComboBox, JLabel, JFrame
from java.awt import Color, GridLayout
from java.awt.event import ActionListener


class Listener(ActionListener):
  def __init__(self, label):
    self.label = label
  def actionPerformed(self, event):
    global frame
    msg = "ActionListener called!"
    self.label.setText(msg)
    frame.pack()


panel = JPanel()

choice_list = ["foo", "bar", "777"]

lbl_foo = JLabel("foo label")
lbl_bar = JLabel("bar label")
panel.add(lbl_foo)
choice = JComboBox(choice_list)
panel.add(choice)
panel.add(lbl_bar)
choice = JComboBox(choice_list)
choice.addActionListener(Listener(lbl_bar))
panel.add(choice)

frame = JFrame("Swing GUI Test Frame")
frame.getContentPane().add(panel)
frame.pack()
frame.setVisible(True)

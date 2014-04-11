from javax.swing import JScrollPane, JPanel, JComboBox, JLabel, JFrame
from java.awt import Color, GridLayout
from java.awt.event import ActionListener

panel = JPanel()
layout = GridLayout(4, 2)
panel.setLayout(layout)

choice_list = ["foo", "bar", "777"]

panel.add(JLabel("foo label"))
choice = JComboBox(choice_list)
panel.add(choice)
panel.add(JLabel("bar label"))
choice = JComboBox(choice_list)
panel.add(choice)

frame = JFrame("JFrame")
frame.getContentPane().add(JScrollPane(panel))
frame.pack()
frame.setVisible(True)
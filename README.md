# UniqueTV

#XML Guide
##Example XML
```
<blocks>
<block name="DC" priority="5" starttime="U1200" endtime="U1730">
	<content order="random" >
		<file path="TV/Arrow/" />
	</content>
	<content order="sequential">
		<file path="TV/Flash/" />
	</content>
</block>
<block name="Movies" priority="3" starttime="M1700" endtime="M2300">
	<content order="random">
		<file path="Movies/" maxduration="120" />
	</content>
</block>
<block name="Background">
	<content>
		<file path="Movies/" genre="Comedy" />
		<file path="TV/" minduration="45" />
	</content>
</block>
</blocks>
```
##Tags
###`<blocks>`
Start and end tag for the xml file. All blocks must be within this tag; anything outside will be discarded.

###`<block>`
Specifies a given block of programming.
Attributes:
- **name:** the name of the block
- **priority:** block priority, to determine which block is played when multiple overlap. Higher priority wins.
- **start:** the start time of the block, in the format [1 letter day code][24 time]. Daycodes are the first letter of the day, with U for Sunday and R for Thursday
- **end:** same as start, but for when the block ends. Blocks can span multiple days.

#`<content>`
Specifies contents within a block. There can be multiple tags within a block; which content to play from is chosen randomly
Attributes:
- **order:** the order files will play in. Either `random`, to play randomly, or `sequential`, to play in order.

#`<file>`



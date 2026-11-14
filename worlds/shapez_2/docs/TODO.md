### Important

- locked tasks are considered in logic in universal tracker with the setting "Lock task lines"
- similarly, operator levels are all considered sphere 1 in the spoiler log, but none of them appear in UT
- some rewards appear to not be supported on operator levels
- not-connected parts in shape layers can fall down individually
- multiple milestone shapes should not be same shapes, because else milestone will appear unlockable while the button does nothing
- update rewards with content bundles
- update location and item names
- surprise ool item can contain keys for nonexistant task lines and operator lines
- fluid miner + extension does not work
- proguseful classification
- Quote: I feel like the the gameplay would flow a lot better if the train unlocks were divided up like this:
  - shape trains (red locomotive, red configurator, rails, immediate stop, wait stop, station spacer, spacer wagon) + (shape wagon, shape loader and unloader)
  - fluid trains (red locomotive, red configurator, rails, immediate stop, wait stop, station spacer, spacer wagon) + (fluid wagon, fluid loader and unloader)
  - progressive train color (multiple instances, each gives you 1 more color of train and configurator) [logic requires you already own 1 of the train packs first]
  - train transfer stations [logic requires you already own 1 of the train packs first]
  - train launcher [logic requires you already own 1 of the train packs first]
  - train vortex delivery [logic requires you to already have launchers first]
- split location_adjustments into milestone/task_line/operator_level_adjustments
- crystal generator needs second floor
- make random checks amount generation happen in generate_early
- research credits are shown x100 and platform capacity x0.5
- look if starting inv from pool needs extra handling
- what about player names with `:`
- Exclude repeated shapes that are generated for milestones from actually being put into the milestones
  - This potentially leads to some milestones having less than 6 or 4 shapes

### Features

- advanced required shapes multiplier
- shape splitter to make vanilla-like milestones possible
- option for additional platform floors
- setting for disabling strict location count checking
- linear upgrades adjustments
- various complexity growth gradients
- scout hints for progression items of other players
- turn output zip into patch file that adds the content to the shapez 2 data folder
- item descriptions
- datapackage settings
- shape upgrader as alternative to downgrader, with option to toggle between both algorithms
- secret code option, effect TBD
- add new 1.0 stuff
- add manufacturer mode

### Technical stuff

- rotation-less direction in shape builder
- put more info into spoiler log
- update tetragonal shape generation to what has been done for hexagonal
- checklist of used processors for downgrader
- add processor types for full cutter and 180 rotator

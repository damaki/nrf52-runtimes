# nRF52 Runtimes

This repository generates Ada/SPARK runtimes for the following SoCs in the
nRF52 series:
* nRF52832
* nRF52833
* nRF52840

The following runtime profiles are supported for of the above:
* light
* light-tasking
* embedded

## Resources Used

The light-tasking and embedded runtime profiles use RTC peripheral to implement
Ada semantics for time, i.e., delay statements and the package Ada.Real_Time.
The RTC interrupt runs at the highest priority. The RTC runs from the low
frequency clock (LFCLK) which runs at 32.768 kHz. The LFCLK source is
configured via the crate configuration, and may be either the external 32 kHz
crystal oscillator (LFXO), the internal 32 kHz oscillator (LFRC), or
synthesized from the 16 MHz high-speed clock (HFCLK).

## Runtime Configuration

The runtime is configurable through the following crate configuration variables:

<table>
  <thead>
    <th>Variable</th>
    <th>Values</th>
    <th>Default</th>
    <th>Description</th>
  </thead>
  <tr>
    <td><tt>Time_Base</tt></td>
    <td>
      <tt>"RTC0"</tt><br/>
      <tt>"RTC1"</tt><br/>
      <tt>"RTC2"</tt><br/>
    </td>
    <td><tt>"RTC2"</tt></td>
    <td>
      Selects which RTC peripheral the runtime uses to implement the semantics
      of `Ada.Real_Time`.
    </td>
  </tr>
  <tr>
    <td><tt>LFCLK_Src</tt></td>
    <td>
      <tt>"Xtal"</tt><br/>
      <tt>"RC"</tt><br/>
      <tt>"Synth"</tt><br/>
    </td>
    <td><tt>"Xtal"</tt></td>
    <td>
      Sets the clock source for the low frequency clock (LFCLK).
      <ul>
        <li><tt>"Xtal"</tt> selects the external 32 kHz crystal as the LFCLK source (LFXO)</li>
        <li><tt>"Rc"</tt> selects the internal LFRC oscillator as the LFCLK source</li>
        <li><tt>"Synth"</tt> synthesises the LFCLK from the HFCLK</li>
      </ul>
    </td>
  </tr>
</table>
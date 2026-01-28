const pptxgen = require('pptxgenjs');
const html2pptx = require('./.github/skills/pptx/scripts/html2pptx');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Tony Chiu';
    pptx.title = 'Site Lead Process Controls Engineer - A Case for Readiness';
    pptx.subject = 'Promotion Discussion - January 30, 2026';

    console.log('Creating slides...');

    // Slide 1: Title
    const { slide: slide1 } = await html2pptx('slides/slide1_title.html', pptx);
    console.log('✓ Slide 1: Title');

    // Slide 2: Today's Objective
    const { slide: slide2 } = await html2pptx('slides/slide2_objective.html', pptx);
    console.log('✓ Slide 2: Objective');

    // Slide 3: Role Understanding
    const { slide: slide3 } = await html2pptx('slides/slide3_role.html', pptx);
    console.log('✓ Slide 3: Role Understanding');

    // Slide 4: Reality Check
    const { slide: slide4 } = await html2pptx('slides/slide4_reality.html', pptx);
    console.log('✓ Slide 4: Reality');

    // Slide 5: Evidence #1 - LARINT01
    const { slide: slide5 } = await html2pptx('slides/slide5_larint01.html', pptx);
    console.log('✓ Slide 5: Evidence #1');

    // Slide 6: Evidence #2 - Alarm Governance
    const { slide: slide6 } = await html2pptx('slides/slide6_alarm.html', pptx);
    console.log('✓ Slide 6: Evidence #2');

    // Slide 7: Evidence #3 - Mark VIe
    const { slide: slide7 } = await html2pptx('slides/slide7_markvie.html', pptx);
    console.log('✓ Slide 7: Evidence #3');

    // Slide 8: Evidence #4 - Budget
    const { slide: slide8 } = await html2pptx('slides/slide8_budget.html', pptx);
    console.log('✓ Slide 8: Evidence #4');

    // Slide 9: Evidence #5 - Talent Development
    const { slide: slide9 } = await html2pptx('slides/slide9_talent.html', pptx);
    console.log('✓ Slide 9: Evidence #5');

    // Slide 10: By the Numbers
    const { slide: slide10 } = await html2pptx('slides/slide10_numbers.html', pptx);
    console.log('✓ Slide 10: Metrics');

    // Slide 11: Stakeholder Validation
    const { slide: slide11 } = await html2pptx('slides/slide11_stakeholders.html', pptx);
    console.log('✓ Slide 11: Stakeholders');

    // Slide 12: What I Bring
    const { slide: slide12 } = await html2pptx('slides/slide12_bring.html', pptx);
    console.log('✓ Slide 12: What I Bring');

    // Slide 13: Addressing Objections
    const { slide: slide13 } = await html2pptx('slides/slide13_objections.html', pptx);
    console.log('✓ Slide 13: Objections');

    // Slide 14: Path Forward
    const { slide: slide14 } = await html2pptx('slides/slide14_path.html', pptx);
    console.log('✓ Slide 14: Path Forward');

    // Slide 15: Closing
    const { slide: slide15 } = await html2pptx('slides/slide15_closing.html', pptx);
    console.log('✓ Slide 15: Closing');

    // Save presentation
    const filename = 'Site_Lead_PCS_Engineer_Presentation_01_30_26.pptx';
    await pptx.writeFile({ fileName: filename });
    console.log(`\n✓ Presentation created successfully: ${filename}`);
}

createPresentation().catch(console.error);
